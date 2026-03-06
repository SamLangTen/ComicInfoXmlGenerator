import unittest
from fastapi.testclient import TestClient
import sys
import os
import json

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.main import app
from src.config_manager import config_manager

class TestAPIConfig(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        # Use a temporary config for testing if possible, 
        # but since config_manager is a singleton, we'll just test the interface
        self.original_config = config_manager.config.copy()

    def tearDown(self):
        # Restore original config
        config_manager.config = self.original_config
        config_manager.save()

    def test_get_config(self):
        response = self.client.get("/api/config")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("llm_base_url", data)
        self.assertIn("llm_api_key", data)

    def test_post_config(self):
        new_settings = {
            "llm_model": "gpt-test-model",
            "appearance_mode": "Light"
        }
        response = self.client.post("/api/config", json=new_settings)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "success"})
        
        # Verify it updated in memory
        self.assertEqual(config_manager.get("llm_model"), "gpt-test-model")
        self.assertEqual(config_manager.get("appearance_mode"), "Light")

if __name__ == "__main__":
    unittest.main()
