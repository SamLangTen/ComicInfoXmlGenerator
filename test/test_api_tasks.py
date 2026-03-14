import unittest
from fastapi.testclient import TestClient
import sys
import os
import tempfile
import shutil
from pathlib import Path

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.main import app
from src.database import DatabaseManager
from src.config_manager import config_manager
import src.database

class TestAPITasks(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_get_data_path = config_manager.get_data_path
        config_manager.get_data_path = lambda x: str(Path(self.test_dir) / x)
        
        # Patch the global db_manager used by API
        import src.database
        import src.api.main
        self.original_db_manager = src.database.db_manager
        self.db_manager = DatabaseManager()
        src.database.db_manager = self.db_manager
        src.api.main.db_manager = self.db_manager
        
        self.client = TestClient(app)

    def tearDown(self):
        import src.database
        import src.api.main
        src.database.db_manager = self.original_db_manager
        src.api.main.db_manager = self.original_db_manager
        config_manager.get_data_path = self.original_get_data_path
        shutil.rmtree(self.test_dir)

    def test_get_tasks_empty(self):
        response = self.client.get("/api/tasks")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_get_tasks_list(self):
        self.db_manager.create_task("scrape", "1.cbz")
        self.db_manager.create_task("scrape", "2.cbz")
        
        response = self.client.get("/api/tasks")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        targets = [t["target"] for t in data]
        self.assertIn("1.cbz", targets)
        self.assertIn("2.cbz", targets)

    def test_get_task_by_id(self):
        task_id = self.db_manager.create_task("scrape", "test.cbz")
        
        response = self.client.get(f"/api/tasks/{task_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], task_id)
        
        response = self.client.get("/api/tasks/999")
        self.assertEqual(response.status_code, 404)

    def test_retry_task(self):
        task_id = self.db_manager.create_task("scrape", "fail.cbz")
        self.db_manager.update_task_status(task_id, "failed")
        
        response = self.client.post(f"/api/tasks/retry/{task_id}")
        self.assertEqual(response.status_code, 200)
        
        task = self.db_manager.get_task(task_id)
        self.assertEqual(task["status"], "pending")

    def test_clear_completed(self):
        t1 = self.db_manager.create_task("scrape", "1.cbz")
        self.db_manager.update_task_status(t1, "completed")
        t2 = self.db_manager.create_task("scrape", "2.cbz")
        self.db_manager.update_task_status(t2, "failed")
        
        response = self.client.delete("/api/tasks/completed")
        self.assertEqual(response.status_code, 200)
        
        tasks = self.db_manager.get_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["id"], t2)

if __name__ == "__main__":
    unittest.main()
