import threading
import time
import json
import logging
import os
import sys
from typing import List, Dict, Any, Optional, Callable

# Add project root to sys.path to allow absolute imports from 'src'
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from src import database
from src.comic_info import ComicInfo
from src.scraper import LocalFilenameScraper, LlmFilenameScraper, BooksScraper
from src.config_manager import config_manager
from dataclasses import asdict

logger = logging.getLogger(__name__)

def scrape_task_handler(task: Dict[str, Any]):
    """Handler for 'scrape' tasks."""
    payload = task.get("payload") or {}
    strategy = payload.get("strategy", "local")
    path = task["target"]
    
    task_logs = []
    def log_callback(msg: str):
        task_logs.append(msg)

    logger.info(f"Starting scrape task {task['id']} for {path} using {strategy} strategy")

    if strategy.lower() == "llm":
        # Get from config_manager or environment variables
        # config_manager.get might return None if key doesn't exist, falling back to env
        api_key = config_manager.get("llm_api_key") or os.environ.get("LLM_API_KEY")
        base_url = config_manager.get("llm_base_url") or os.environ.get("LLM_BASE_URL")
        model = config_manager.get("llm_model") or os.environ.get("LLM_MODEL")
        
        # Log configuration status (don't log actual keys)
        if not api_key:
            log_callback("[LLM] Warning: LLM_API_KEY is not set.")
        
        scraper = LlmFilenameScraper(
            api_key=api_key,
            base_url=base_url,
            model=model
        )
    elif strategy.lower() == "books":
        scraper = BooksScraper()
    else:
        scraper = LocalFilenameScraper()

    # 1. Load existing metadata from DB or create new
    cached = database.db_manager.get_archive(path)
    if cached:
        comic = ComicInfo.from_dict(cached["metadata"])
    else:
        comic = ComicInfo(path=path)

    # 2. Perform scrape
    # For specialized scrapers, ensure we at least have some basic metadata from filename
    if strategy.lower() != "local" and not (comic.Title or comic.Series):
        log_callback(f"[System] Pre-populating metadata using LocalFilenameScraper")
        LocalFilenameScraper().search(comic)

    try:
        scraper.search(comic, log_callback=log_callback)
    except Exception as e:
        log_callback(f"[Error] Scraper failure: {str(e)}")
        logger.exception(f"Scraper error in task {task['id']}")

    # 3. Update DB
    if comic.path:
        mtime = os.path.getmtime(comic.path)
        database.db_manager.update_archive(comic.path, mtime, comic.Series, asdict(comic))

    return {
        "status": "success", 
        "series": comic.Series,
        "logs": "\n".join(task_logs)
    }

class TaskPool:
    def __init__(self, max_workers: int = 4, db_manager=None, max_retries: int = 3, status_change_callback: Optional[Callable[[Dict[str, Any]], None]] = None):
        self.max_workers = max_workers
        self.max_retries = max_retries
        self.db_manager = db_manager or database.db_manager
        self.status_change_callback = status_change_callback
        self.workers: List[threading.Thread] = []
        self._stop_event = threading.Event()
        self._condition = threading.Condition()
        self._db_lock = threading.Lock()
        self._active_tasks = 0
        self._task_handlers: Dict[str, Callable] = {
            "scrape": scrape_task_handler
        }

        self._recover_tasks()
        self._start_workers()

    def _recover_tasks(self):
        """Resets 'running' tasks to 'pending' on startup."""
        running = self.db_manager.get_tasks(status="running", limit=1000)
        for task in running:
            logger.info(f"Recovering interrupted task {task['id']} (resetting to pending)")
            self.db_manager.update_task_status(task["id"], "pending")


    def _start_workers(self):
        for i in range(self.max_workers):
            t = threading.Thread(target=self._worker_loop, name=f"TaskWorker-{i}")
            t.daemon = True
            t.start()
            self.workers.append(t)

    def register_handler(self, task_type: str, handler: Callable):
        """Registers a handler for a specific task type."""
        self._task_handlers[task_type] = handler

    def submit(self, type: str, target: str, payload: Optional[Dict[str, Any]] = None) -> int:
        """Submits a new task to the database and signals workers."""
        task_id = self.db_manager.create_task(type, target, payload)
        self._notify_status_change(task_id)
        with self._condition:
            self._condition.notify_all()
        return task_id

    def _notify_status_change(self, task_id: int):
        """Notifies the callback about a task status change."""
        if self.status_change_callback:
            task = self.db_manager.get_task(task_id)
            if task:
                try:
                    self.status_change_callback(task)
                except Exception as e:
                    logger.error(f"Error in status change callback: {e}")

    def stop(self):
        """Stops the task pool."""
        self._stop_event.set()
        with self._condition:
            self._condition.notify_all()
        for t in self.workers:
            t.join(timeout=1.0)

    def _worker_loop(self):
        while not self._stop_event.is_set():
            task = None
            with self._condition:
                # Only pick up a task if we have capacity and there's work
                while not self._stop_event.is_set():
                    if self._active_tasks < self.max_workers:
                        with self._db_lock:
                            # We'll use the DB to find pending tasks
                            pending = self.db_manager.get_tasks(status="pending", limit=1)
                            if pending:
                                task = pending[0]
                                # Mark it as running immediately to prevent other workers from picking it up
                                self.db_manager.update_task_status(task["id"], "running")
                                self._active_tasks += 1
                                self._notify_status_change(task["id"])
                                break
                    
                    self._condition.wait(timeout=1.0)

            if task:
                try:
                    self._process_task(task)
                    self._notify_status_change(task["id"])
                except Exception as e:
                    logger.exception(f"Error processing task {task['id']}: {e}")
                    
                    # Retry logic
                    current_retries = task.get("retries", 0)
                    if current_retries < self.max_retries:
                        logger.info(f"Retrying task {task['id']} (attempt {current_retries + 1}/{self.max_retries})")
                        self.db_manager.increment_task_retries(task["id"])
                        self.db_manager.update_task_status(task["id"], "pending", result={"error": str(e)})
                    else:
                        logger.error(f"Task {task['id']} failed after {current_retries} retries")
                        self.db_manager.update_task_status(task["id"], "failed", result={"error": str(e)})
                    
                    self._notify_status_change(task["id"])
                finally:
                    with self._condition:
                        self._active_tasks -= 1
                        self._condition.notify_all()

    def _process_task(self, task: Dict[str, Any]):
        task_type = task["type"]
        handler = self._task_handlers.get(task_type)
        if not handler:
            raise ValueError(f"No handler registered for task type: {task_type}")
        
        result = handler(task)
        self.db_manager.update_task_status(task["id"], "completed", result=result)

# Global singleton
task_pool = None

def init_task_pool(max_workers: int = 4, max_retries: int = 3, status_change_callback: Optional[Callable[[Dict[str, Any]], None]] = None):
    global task_pool
    if task_pool is None:
        task_pool = TaskPool(max_workers=max_workers, max_retries=max_retries, status_change_callback=status_change_callback)
    return task_pool
