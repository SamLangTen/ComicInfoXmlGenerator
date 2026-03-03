import os
import json
import httpx
from src.comic_info import ComicInfo
from src.config import LLM_BASE_URL, LLM_API_KEY, LLM_MODEL

class LlmFilenameScraper:
    """
    Scraper that uses an LLM to parse comic metadata from the filename.
    """

    def __init__(self, model: str = LLM_MODEL, base_url: str = LLM_BASE_URL, api_key: str = LLM_API_KEY) -> None:
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.system_prompt = (
            "You are a comic metadata expert. Analyze the given filename and extract metadata. "
            "Return ONLY a JSON object with keys: Series, Number, Volume, Year. "
            "Volume and Year should be integers (-1 if unknown). Number should be a string."
        )

    def search(self, comic: ComicInfo) -> ComicInfo:
        if not comic.path or not self.api_key:
            return comic

        filename = os.path.basename(comic.path)
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Filename: {filename}"}
            ]
            payload = {
                "model": self.model,
                "messages": messages,
                "response_format": {"type": "json_object"}
            }

            # Log prompt for debugging
            print("\n" + "="*50)
            print("LLM SCRAPER REQUEST")
            print(f"URL: {self.base_url}/chat/completions")
            print(f"Model: {self.model}")
            print(f"System Prompt: {self.system_prompt}")
            print(f"User Message: Filename: {filename}")
            print("="*50 + "\n")

            response = httpx.post(f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=30.0)
            response.raise_for_status()
            
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            metadata = json.loads(content)

            comic.Series = metadata.get("Series", comic.Series)
            comic.Number = metadata.get("Number", comic.Number)
            comic.Volume = metadata.get("Volume", comic.Volume)
            comic.Year = metadata.get("Year", comic.Year)

        except Exception as e:
            print(f"LLM Scraper error: {e}")

        return comic
