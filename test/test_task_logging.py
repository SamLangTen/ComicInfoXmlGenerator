
import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.task_manager import scrape_task_handler
from src.comic_info import ComicInfo

class TestTaskLogging(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        patcher = patch('src.database.db_manager', self.mock_db)
        patcher.start()
        self.addCleanup(patcher.stop)

    @patch('src.scraper.books_scraper.BooksScraper.search')
    def test_scrape_task_handler_logs_captured(self, mock_search):
        # 1. Setup mock task and data
        task = {
            "id": 1,
            "type": "scrape",
            "target": "test_data/test.cbz",
            "payload": {"strategy": "books"}
        }
        
        # Mock database.db_manager.get_archive to return None (new file)
        self.mock_db.get_archive.return_value = None
        
        # Simulate scraper behavior: it should call log_callback
        def side_effect(comic, log_callback=None):
            if log_callback:
                log_callback("Starting search...")
                log_callback("Found result: Frieren 01")
            comic.Series = "Frieren"
            return comic
        
        mock_search.side_effect = side_effect

        # 2. Run handler
        # We need to mock os.path.getmtime and database.db_manager.update_archive
        with patch('os.path.getmtime', return_value=123456.0):
            result = scrape_task_handler(task)

        # 3. Assertions
        # Check if logs were stored in the return result (this is where current handler returns data)
        # OR better: check if handler passed a callback that eventually updates the task log in DB.
        # According to Phase 1 spec: "verify that the result field contains full logs".
        
        self.assertIn("logs", result, "Result should contain 'logs' key")
        self.assertIn("Starting search...", result["logs"])
        self.assertIn("Found result: Frieren 01", result["logs"])
        self.assertEqual(result["series"], "Frieren")

if __name__ == "__main__":
    unittest.main()
