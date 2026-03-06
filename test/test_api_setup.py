import unittest
from fastapi.testclient import TestClient
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestAPISetup(unittest.TestCase):
    def setUp(self):
        try:
            from src.api.main import app
            self.client = TestClient(app)
        except ImportError:
            self.app_exists = False
        else:
            self.app_exists = True

    def test_health_check(self):
        if not self.app_exists:
            self.fail("src.api.main.app not found")
        
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

if __name__ == "__main__":
    unittest.main()
