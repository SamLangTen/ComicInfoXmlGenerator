import unittest
from fastapi.testclient import TestClient
import sys
import os
import tempfile
import shutil
import time
from pathlib import Path

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.main import app
from src.comic_info import ComicInfo
from src.database import DatabaseManager
from src.config_manager import config_manager
import src.database
import src.api.main
import src.task_manager
from src.task_manager import init_task_pool

class TestAPIScrape(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_get_data_path = config_manager.get_data_path
        config_manager.get_data_path = lambda x: str(Path(self.test_dir) / x)
        
        # Patch the global db_manager
        self.original_db_manager = src.database.db_manager
        self.db_manager = DatabaseManager()
        src.database.db_manager = self.db_manager
        src.api.main.db_manager = self.db_manager
        
        # Initialize task pool
        self.task_pool = init_task_pool(max_workers=2)
        
        self.client = TestClient(app)
        self.files = ["Batman 001.cbz", "Superman 002.cbz"]
        self.full_paths = []
        for f in self.files:
            p = os.path.join(self.test_dir, f)
            with open(p, 'w') as tmp:
                tmp.write("data")
            self.full_paths.append(p)

    def tearDown(self):
        self.task_pool.stop()
        src.database.db_manager = self.original_db_manager
        src.api.main.db_manager = self.original_db_manager
        config_manager.get_data_path = self.original_get_data_path
        shutil.rmtree(self.test_dir)
        src.task_manager.task_pool = None

    def test_batch_scrape(self):
        # Use 'local' strategy which is fast and local
        response = self.client.post("/api/scrape", json={
            "paths": self.full_paths,
            "strategy": "local"
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(len(data["task_ids"]), 2)
        
        # Wait for tasks to complete
        timeout = 5.0
        start_time = time.time()
        while time.time() - start_time < timeout:
            pending = self.db_manager.get_tasks(status="pending")
            running = self.db_manager.get_tasks(status="running")
            if not pending and not running:
                break
            time.sleep(0.1)
        
        # Verify DB was updated
        archive1 = self.db_manager.get_archive(self.full_paths[0])
        archive2 = self.db_manager.get_archive(self.full_paths[1])
        self.assertIsNotNone(archive1)
        self.assertIsNotNone(archive2)
        self.assertEqual(archive1["series_name"], "Batman")
        self.assertEqual(archive2["series_name"], "Superman")

if __name__ == "__main__":
    unittest.main()
