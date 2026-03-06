import unittest
from fastapi.testclient import TestClient
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.main import app

class TestAPIMetadata(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.test_path = "/path/to/comic.cbz"

    def test_metadata_lifecycle(self):
        # 1. Get non-existent metadata (should return default or 404?)
        # Let's say it returns a new ComicInfo object with that path.
        response = self.client.get(f"/api/metadata?path={self.test_path}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["path"], self.test_path)
        self.assertEqual(data["Series"], "")

        # 2. Update metadata
        update_data = {
            "path": self.test_path,
            "Series": "Test Series",
            "Number": "123",
            "Writer": "Test Writer"
        }
        response = self.client.post("/api/metadata", json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "success"})

        # 3. Get again, verify it's cached
        response = self.client.get(f"/api/metadata?path={self.test_path}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["Series"], "Test Series")
        self.assertEqual(data["Number"], "123")
        self.assertEqual(data["Writer"], "Test Writer")

if __name__ == "__main__":
    unittest.main()
