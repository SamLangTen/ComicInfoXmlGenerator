import unittest
import time
import tempfile
import shutil
import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import DatabaseManager
from src.config_manager import config_manager
from src.task_manager import TaskPool
import src.database

class TestEndToEndParallel(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_get_data_path = config_manager.get_data_path
        config_manager.get_data_path = lambda x: str(Path(self.test_dir) / x)
        
        # Patch the global db_manager
        self.original_db_manager = src.database.db_manager
        self.db_manager = DatabaseManager()
        src.database.db_manager = self.db_manager
        
        # Initialize task pool with 4 workers
        self.task_pool = TaskPool(max_workers=4, db_manager=self.db_manager)

    def tearDown(self):
        self.task_pool.stop()
        src.database.db_manager = self.original_db_manager
        config_manager.get_data_path = self.original_get_data_path
        shutil.rmtree(self.test_dir)

    def test_parallel_load(self):
        # 1. Create 20 mock comic files
        num_tasks = 20
        test_files = []
        for i in range(num_tasks):
            p = Path(self.test_dir) / f"ComicSeries{i:03d} 001.cbz"
            p.touch()
            test_files.append(str(p))
            
        # 2. Submit all tasks
        task_ids = []
        for p in test_files:
            tid = self.task_pool.submit("scrape", p, {"strategy": "local"})
            task_ids.append(tid)
            
        # 3. Wait for all to complete
        timeout = 10.0
        start_time = time.time()
        while time.time() - start_time < timeout:
            pending = self.db_manager.get_tasks(status="pending")
            running = self.db_manager.get_tasks(status="running")
            if not pending and not running:
                break
            time.sleep(0.2)
            
        # 4. Verify results
        all_tasks = self.db_manager.get_tasks(limit=100)
        self.assertEqual(len(all_tasks), num_tasks)
        
        completed = [t for t in all_tasks if t["status"] == "completed"]
        self.assertEqual(len(completed), num_tasks)
        
        for i in range(num_tasks):
            archive = self.db_manager.get_archive(test_files[i])
            self.assertIsNotNone(archive)
            # Just verify it parsed something related to our name
            self.assertTrue(archive["series_name"].startswith("ComicSeries"))

if __name__ == "__main__":
    unittest.main()
