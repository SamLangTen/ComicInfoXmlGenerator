
import unittest
from unittest.mock import MagicMock, patch
import os
import sys
import json
from dataclasses import asdict

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.comic_info import ComicInfo

class TestDbSync(unittest.TestCase):
    def setUp(self):
        # We need to mock the database and the session_cache in src.api.main
        self.mock_db = MagicMock()
        
        # Patching db_manager
        patcher_db = patch('src.api.main.db_manager', self.mock_db)
        patcher_db.start()
        self.addCleanup(patcher_db.stop)

    async def test_api_metadata_reflects_db_update(self):
        # This is an async test because FastAPI endpoints are async
        from src.api.main import get_metadata
        
        test_path = "test.cbz"
        
        # 1. First call: DB has old data
        old_meta = asdict(ComicInfo(Title="Old Title", Series="Old Series"))
        self.mock_db.get_archive.return_value = {"metadata": old_meta}
        
        first_resp = await get_metadata(test_path)
        self.assertEqual(first_resp["Title"], "Old Title")

        # 2. Simulate Background Task updates DB
        new_meta = asdict(ComicInfo(Title="New Title", Series="New Series"))
        # DB now would return new data
        self.mock_db.get_archive.return_value = {"metadata": new_meta}
        
        # 3. Second call: Should reflect new data immediately as cache is gone
        second_resp = await get_metadata(test_path)
        
        self.assertEqual(second_resp["Title"], "New Title", "API should return updated metadata from DB")

if __name__ == "__main__":
    # Since we have async test, use a simple runner or wrap it
    import asyncio
    def run_async_test(coro):
        return asyncio.run(coro)
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDbSync)
    # We'll manually run the test since it's async
    test_instance = TestDbSync()
    test_instance.setUp()
    try:
        asyncio.run(test_instance.test_api_metadata_reflects_db_update())
        print("SUCCESS: test_api_metadata_reflects_db_update passed")
    except AssertionError as e:
        print(f"FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
