import json
import os
from pathlib import Path

class ConfigManager:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = Path(config_path)
        self.defaults = {
            "llm_base_url": "https://api.openai.com/v1",
            "llm_api_key": "",
            "llm_model": "gpt-4o-mini",
            "appearance_mode": "System",
            "default_scraper": "Local",
            "manga_root_directory": "",
            "auto_scan_enabled": True,
            "auto_scan_interval_minutes": 30,
            "data_directory": "data" # Default to a local 'data' folder
        }
        self.config = self.defaults.copy()
        self.load()
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        data_dir = Path(self.get("data_directory"))
        data_dir.mkdir(parents=True, exist_ok=True)
        (data_dir / "cache" / "covers").mkdir(parents=True, exist_ok=True)

    def get_data_path(self, sub_path: str) -> Path:
        """Helper to get a path relative to the data directory."""
        return Path(self.get("data_directory")) / sub_path

    def load(self):
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    user_config = json.load(f)
                    self.config.update(user_config)
            except Exception as e:
                print(f"Error loading config: {e}")

    def save(self):
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get(self, key: str):
        return self.config.get(key, self.defaults.get(key))

    def set(self, key: str, value: str):
        self.config[key] = value
        self.save()

# Global singleton instance
config_manager = ConfigManager()
