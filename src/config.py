import os
from dotenv import load_dotenv
from src.config_manager import config_manager

# Load .env file if it exists for backward compatibility
load_dotenv()

def get_env(key: str, default: str = "") -> str:
    """Get an environment variable or return a default value."""
    return os.environ.get(key, default)

# LLM Configuration (Dynamically linked to config_manager)
LLM_BASE_URL = config_manager.get("llm_base_url") or get_env("LLM_BASE_URL", "https://api.openai.com/v1")
LLM_API_KEY = config_manager.get("llm_api_key") or get_env("LLM_API_KEY", "")
LLM_MODEL = config_manager.get("llm_model") or get_env("LLM_MODEL", "gpt-4o-mini")
