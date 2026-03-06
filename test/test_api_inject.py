import unittest
from fastapi.testclient import TestClient
import sys
import os
import tempfile
import shutil
import zipfile

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.main import app, session_cache
from src.comic_info import ComicInfo

class TestAPIInject(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.test_dir = tempfile.mkdtemp()
        self.cbz_path = os.path.join(self.test_dir, "test.cbz")
        with zipfile.ZipFile(self.cbz_path, 'w') as zf:
            zf.writestr("page1.jpg", b"data")
        
        # Pre-populate cache with metadata
        comic = ComicInfo(path=self.cbz_path, Series="Test Series", Number="1")
        session_cache[self.cbz_path] = comic

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        session_cache.clear()

    def test_inject_metadata(self):
        response = self.client.post("/api/inject", json={"paths": [self.cbz_path]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "success", "results": {self.cbz_path: "success"}})
        
        # Verify XML exists in the zip
        with zipfile.ZipFile(self.cbz_path, 'r') as zf:
            self.assertIn("ComicInfo.xml", zf.namelist())
            xml_content = zf.read("ComicInfo.xml").decode("utf-8")
            self.assertIn("<Series>Test Series</Series>", xml_content)

if __name__ == "__main__":
    unittest.main()
