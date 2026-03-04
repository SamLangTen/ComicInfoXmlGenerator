import os
import json
import httpx
from typing import List, Optional, Callable
from src.comic_info import ComicInfo
from src.config import LLM_BASE_URL, LLM_API_KEY, LLM_MODEL

class LlmFilenameScraper:
    """
    Scraper that uses an LLM to parse comic metadata from the filename.
    Supports batch processing to save tokens and time.
    """

    def __init__(self, model: str = LLM_MODEL, base_url: str = LLM_BASE_URL, api_key: str = LLM_API_KEY) -> None:
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.system_prompt = (
            "You are a comic metadata expert. Analyze the given list of filenames and extract as much metadata as possible for EACH file.\n"
            "Return a JSON object with a single key 'comics' containing an array of objects.\n"
            "Each object MUST have these keys: Filename (exact filename from input), Series, Number, Volume, Year, Month, Day, Writer, Penciller, Inker, Colorist, Letterer, CoverArtist, Editor, "
            "Publisher, Imprint, Genre, AgeRating, Characters, Teams, Locations, ScanInformation, StoryArc, SeriesGroup, Web, BlackAndWhite, Manga.\n\n"
            "Rules:\n"
            "1. For Year, Month, Day, and Volume, use integers (-1 if unknown).\n"
            "2. For others, use strings (empty string if unknown).\n"
            "3. For BlackAndWhite and Manga, use 'Yes', 'No', or 'Unknown'.\n"
            "4. CRITICAL: If you identify a general author/creator in the filename but their specific role (e.g., Writer, Penciller) is not mentioned, "
            "assign that person to BOTH the 'Writer' and 'Penciller' fields.\n"
            "5. If a specific chapter/issue title is not found, use the combination of 'Series' and 'Volume' (e.g., 'Series Name Vol. 1') as the 'Title'.\n"
            "6. Look carefully at all text in brackets [ ] or parentheses ( ) for possible creator names, publishers, or scan groups.\n\n"
            "Example Result:\n"
            "{\n"
            "  \"comics\": [\n"
            "    {\"Filename\": \"file1.cbz\", \"Series\": \"Spider-Man\", \"Number\": \"01\", \"Year\": 1962 ...},\n"
            "    {\"Filename\": \"file2.cbz\", \"Series\": \"X-Men\", \"Number\": \"05\", \"Year\": 1963 ...}\n"
            "  ]\n"
            "}"
        )

    def _apply_metadata(self, comic: ComicInfo, metadata: dict):
        fields = [
            "Title", "Series", "Number", "Volume", "Year", "Month", "Day", 
            "Writer", "Penciller", "Inker", "Colorist", "Letterer", "CoverArtist", "Editor",
            "Publisher", "Imprint", "Genre", "AgeRating", "Characters", "Teams", "Locations",
            "ScanInformation", "StoryArc", "SeriesGroup", "Web", "BlackAndWhite", "Manga"
        ]
        for field in fields:
            if field in metadata:
                setattr(comic, field, metadata[field])

    def search(self, comic: ComicInfo, log_callback: Optional[Callable[[str], None]] = None) -> ComicInfo:
        """Single item search - falls back to search_batch logic."""
        results = self.search_batch([comic], log_callback=log_callback)
        return results[0]

    def search_batch(self, comics: List[ComicInfo], log_callback: Optional[Callable[[str], None]] = None) -> List[ComicInfo]:
        if not comics or not self.api_key:
            return comics

        # Batch in chunks of 10 to avoid context limits
        chunk_size = 10
        for i in range(0, len(comics), chunk_size):
            chunk = comics[i : i + chunk_size]
            filenames = [os.path.basename(c.path) for c in chunk if c.path]
            
            try:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                messages = [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Filenames: {json.dumps(filenames, ensure_ascii=False)}"}
                ]
                payload = {
                    "model": self.model,
                    "messages": messages,
                    "response_format": {"type": "json_object"}
                }

                # Prepare detailed logs
                log_header = f"--- LLM BATCH REQUEST ({len(chunk)} files) ---"
                payload_str = json.dumps(payload, indent=2, ensure_ascii=False)
                
                # Log to terminal
                print(f"\n{log_header}\n{payload_str}\n")
                
                # Log to GUI via callback
                if log_callback:
                    log_callback(f"\n[REQUEST]\n{log_header}\n{payload_str}\n")

                response = httpx.post(f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=60.0)
                response.raise_for_status()
                
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                
                # Log response
                print(f"--- LLM RESPONSE ---\n{content}\n")
                if log_callback:
                    log_callback(f"\n[RESPONSE]\n{content}\n")

                # Parse content
                try:
                    data_parsed = json.loads(content)
                except json.JSONDecodeError as je:
                    error_msg = f"LLM JSON Decode Error: {je}"
                    print(error_msg)
                    if log_callback: log_callback(f"\n[ERROR] {error_msg}\n")
                    continue

                metadata_list = []
                if isinstance(data_parsed, list):
                    metadata_list = data_parsed
                elif isinstance(data_parsed, dict):
                    if "comics" in data_parsed and isinstance(data_parsed["comics"], list):
                        metadata_list = data_parsed["comics"]
                    else:
                        for key in data_parsed:
                            if isinstance(data_parsed[key], list):
                                metadata_list = data_parsed[key]
                                break
                        if not metadata_list:
                            metadata_list = [data_parsed]
                
                if isinstance(metadata_list, list):
                    for metadata in metadata_list:
                        fname = metadata.get("Filename")
                        if fname:
                            for c in chunk:
                                if os.path.basename(c.path) == fname:
                                    self._apply_metadata(c, metadata)
                                    break
                else:
                    print(f"LLM Error: Failed to extract list. Got {type(data_parsed)}")

            except Exception as e:
                error_msg = f"LLM Batch error: {e}"
                print(error_msg)
                if log_callback: log_callback(f"\n[ERROR] {error_msg}\n")

        return comics
