import unittest
from fastapi.testclient import TestClient
import sys
import os
import tempfile
import shutil

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.main import app

class TestAPIScan(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.test_dir = tempfile.mkdtemp()
        # Create some mock archives
        self.files = ["comic1.cbz", "comic2.cbr"]
        for f in self.files:
            with open(os.path.join(self.test_dir, f), 'w') as tmp:
                tmp.write("data")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_scan_archives(self):
        response = self.client.post("/api/scan", json={"directory": self.test_dir})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("files", data)
        self.assertEqual(len(data["files"]), 2)
        # Check if filenames are in the list (as relative paths or full paths?)
        # Let's assume full paths for now or whatever scan_archives returns.
        found_basenames = [os.path.basename(f) for f in data["files"]]
        for f in self.files:
            self.assertIn(f, found_basenames)

if __name__ == "__main__":
    unittest.main()
