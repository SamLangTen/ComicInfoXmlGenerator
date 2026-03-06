import unittest
from fastapi.testclient import TestClient
import sys
import os
import tempfile
import shutil

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.main import app, session_cache
from src.comic_info import ComicInfo

class TestAPIScrape(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.test_dir = tempfile.mkdtemp()
        self.files = ["Batman 001.cbz", "Superman 002.cbz"]
        self.full_paths = []
        for f in self.files:
            p = os.path.join(self.test_dir, f)
            with open(p, 'w') as tmp:
                tmp.write("data")
            self.full_paths.append(p)
            # Pre-populate cache
            session_cache[p] = ComicInfo(path=p)

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        session_cache.clear()

    def test_batch_scrape(self):
        # Use 'regex' strategy which is fast and local
        response = self.client.post("/api/scrape", json={
            "paths": self.full_paths,
            "strategy": "regex"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "success"})
        
        # Verify cache was updated
        self.assertEqual(session_cache[self.full_paths[0]].Series, "Batman")
        self.assertEqual(session_cache[self.full_paths[1]].Series, "Superman")

if __name__ == "__main__":
    unittest.main()
