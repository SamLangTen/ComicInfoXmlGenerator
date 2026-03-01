import os
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()

def get_env(key: str, default: str = "") -> str:
    """Get an environment variable or return a default value."""
    return os.environ.get(key, default)

# LLM Configuration
LLM_BASE_URL = get_env("LLM_BASE_URL", "https://api.openai.com/v1")
LLM_API_KEY = get_env("LLM_API_KEY", "")
LLM_MODEL = get_env("LLM_MODEL", "gpt-4o-mini")
