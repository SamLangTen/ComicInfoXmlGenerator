import unittest
import time
import tempfile
import shutil
from pathlib import Path
from src.database import DatabaseManager
from src.config_manager import config_manager
from src.task_manager import TaskPool

class MockWorker:
    def __init__(self, task):
        self.task = task
    def run(self):
        time.sleep(0.1)
        return {"success": True}

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_get_data_path = config_manager.get_data_path
        config_manager.get_data_path = lambda x: str(Path(self.test_dir) / x)
        
        # Patch the global db_manager
        import src.database
        self.original_db_manager = src.database.db_manager
        self.db_manager = DatabaseManager()
        src.database.db_manager = self.db_manager
        
        self.task_pool = TaskPool(max_workers=2, db_manager=self.db_manager)

    def tearDown(self):
        self.task_pool.stop()
        import src.database
        src.database.db_manager = self.original_db_manager
        config_manager.get_data_path = self.original_get_data_path
        shutil.rmtree(self.test_dir)

    def test_submit_task(self):
        task_id = self.task_pool.submit("scrape", "/path/1", {"scraper": "test"})
        self.assertIsNotNone(task_id)
        
        task = self.db_manager.get_task(task_id)
        self.assertIn(task["status"], ["pending", "running", "failed"])
        self.assertEqual(task["target"], "/path/1")

    def test_worker_lifecycle_basic(self):
        # Register a simple handler
        results = []
        def test_handler(task):
            results.append(task["target"])
            return {"processed": True}
        
        self.task_pool.register_handler("scrape", test_handler)
        
        # Submit task
        task_id = self.task_pool.submit("scrape", "/path/test")
        
        # Wait for task to be processed (it should be very fast)
        timeout = 2.0
        start_time = time.time()
        while time.time() - start_time < timeout:
            task = self.db_manager.get_task(task_id)
            if task["status"] == "completed":
                break
            time.sleep(0.1)
            
        self.assertEqual(task["status"], "completed")
        self.assertEqual(task["result"], {"processed": True})
        self.assertIn("/path/test", results)

    def test_worker_parallelism(self):
        # Register a handler that sleeps
        import threading
        active_count = 0
        max_active = 0
        lock = threading.Lock()

        def slow_handler(task):
            nonlocal active_count, max_active
            with lock:
                active_count += 1
                max_active = max(max_active, active_count)
            time.sleep(0.5)
            with lock:
                active_count -= 1
            return {"done": True}

        self.task_pool.register_handler("scrape", slow_handler)
        
        # Submit 3 tasks (max_workers is 2 in setUp)
        t1 = self.task_pool.submit("scrape", "1")
        t2 = self.task_pool.submit("scrape", "2")
        t3 = self.task_pool.submit("scrape", "3")
        
        # Wait for all to finish
        timeout = 5.0
        start_time = time.time()
        while time.time() - start_time < timeout:
            pending = self.db_manager.get_tasks(status="pending")
            running = self.db_manager.get_tasks(status="running")
            if not pending and not running:
                break
            time.sleep(0.1)
            
        self.assertEqual(max_active, 2) # Confirm only 2 ran at once
        self.assertEqual(self.db_manager.get_task(t3)["status"], "completed")

    def test_scrape_task_execution(self):
        # Create a mock comic file
        comic_path = Path(self.test_dir) / "Amazing Spider-Man v1 001.cbz"
        comic_path.touch()
        
        # Submit scrape task
        task_id = self.task_pool.submit("scrape", str(comic_path), {"strategy": "local"})
        
        # Wait for completion
        timeout = 5.0
        start_time = time.time()
        while time.time() - start_time < timeout:
            task = self.db_manager.get_task(task_id)
            if task["status"] == "completed":
                break
            time.sleep(0.1)
            
        self.assertEqual(task["status"], "completed")
        self.assertEqual(task["result"]["status"], "success")
        
        # Verify DB was updated
        archive = self.db_manager.get_archive(str(comic_path))
        self.assertIsNotNone(archive)
        self.assertEqual(archive["series_name"], "Amazing Spider-Man") # Local scraper output

    def test_init_task_pool(self):
        from src.task_manager import init_task_pool, task_pool
        # Reset global task_pool for testing
        import src.task_manager
        src.task_manager.task_pool = None
        
        pool = init_task_pool(max_workers=3)
        self.assertIsNotNone(pool)
        self.assertEqual(pool.max_workers, 3)
        
        # Calling again should return the same pool
        pool2 = init_task_pool(max_workers=5)
        self.assertEqual(pool, pool2)
        self.assertEqual(pool2.max_workers, 3) # Should not have changed
        
        pool.stop()

if __name__ == "__main__":
    unittest.main()
