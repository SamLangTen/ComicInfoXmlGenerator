import threading
import time
import json
import logging
import os
from typing import List, Dict, Any, Optional, Callable
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

    logger.info(f"Starting scrape task {task['id']} for {path} using {strategy} strategy")

    if strategy.lower() == "llm":
        scraper = LlmFilenameScraper(
            api_key=config_manager.get("llm_api_key"),
            base_url=config_manager.get("llm_base_url"),
            model=config_manager.get("llm_model")
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
    scraper.search(comic)

    # 3. Update DB
    if comic.path:
        mtime = os.path.getmtime(comic.path)
        database.db_manager.update_archive(comic.path, mtime, comic.Series, asdict(comic))

    return {"status": "success", "series": comic.Series}

class TaskPool:
    def __init__(self, max_workers: int = 4, db_manager=None):
        self.max_workers = max_workers
        self.db_manager = db_manager or database.db_manager
        self.workers: List[threading.Thread] = []
        self._stop_event = threading.Event()
        self._condition = threading.Condition()
        self._db_lock = threading.Lock()
        self._active_tasks = 0
        self._task_handlers: Dict[str, Callable] = {
            "scrape": scrape_task_handler
        }

        self._start_workers()


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
        with self._condition:
            self._condition.notify_all()
        return task_id

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
                                break
                    
                    self._condition.wait(timeout=1.0)

            if task:
                try:
                    self._process_task(task)
                except Exception as e:
                    logger.exception(f"Error processing task {task['id']}: {e}")
                    self.db_manager.update_task_status(task["id"], "failed", result={"error": str(e)})
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

def init_task_pool(max_workers: int = 4):
    global task_pool
    if task_pool is None:
        task_pool = TaskPool(max_workers=max_workers)
    return task_pool
