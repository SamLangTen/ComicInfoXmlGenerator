import unittest
import sqlite3
import json
import tempfile
import shutil
from pathlib import Path
from src.database import DatabaseManager
from src.config_manager import config_manager

class TestTaskDatabase(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for tests
        self.test_dir = tempfile.mkdtemp()
        self.config_patch = {
            "data_path": self.test_dir
        }
        # Mocking config_manager.get_data_path to use our temp dir
        self.original_get_data_path = config_manager.get_data_path
        config_manager.get_data_path = lambda x: str(Path(self.test_dir) / x)
        
        self.db_manager = DatabaseManager()

    def tearDown(self):
        # Restore original get_data_path
        config_manager.get_data_path = self.original_get_data_path
        shutil.rmtree(self.test_dir)

    def test_create_task(self):
        task_id = self.db_manager.create_task(
            type="scrape",
            target="/path/to/comic.cbz",
            payload={"scraper": "llm"}
        )
        self.assertIsNotNone(task_id)
        
        task = self.db_manager.get_task(task_id)
        self.assertEqual(task["type"], "scrape")
        self.assertEqual(task["target"], "/path/to/comic.cbz")
        self.assertEqual(task["status"], "pending")
        self.assertEqual(task["payload"], {"scraper": "llm"})

    def test_update_task_status(self):
        task_id = self.db_manager.create_task("scrape", "/path/to/comic.cbz")
        self.db_manager.update_task_status(task_id, "running")
        
        task = self.db_manager.get_task(task_id)
        self.assertEqual(task["status"], "running")
        
        self.db_manager.update_task_status(task_id, "completed", result={"success": True})
        task = self.db_manager.get_task(task_id)
        self.assertEqual(task["status"], "completed")
        self.assertEqual(task["result"], {"success": True})

    def test_get_non_existent_task(self):
        task = self.db_manager.get_task(999)
        self.assertIsNone(task)

    def test_get_tasks_no_filter(self):
        self.db_manager.create_task("scrape", "1.cbz")
        self.db_manager.create_task("scrape", "2.cbz")
        
        all_tasks = self.db_manager.get_tasks()
        self.assertEqual(len(all_tasks), 2)

    def test_get_pending_tasks(self):
        self.db_manager.create_task("scrape", "1.cbz")
        self.db_manager.create_task("scrape", "2.cbz")
        
        pending = self.db_manager.get_tasks(status="pending")
        self.assertEqual(len(pending), 2)

if __name__ == "__main__":
    unittest.main()
