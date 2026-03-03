import re
import os
import json
import httpx
from typing import List
from src.comic_info import ComicInfo
from src.config import LLM_BASE_URL, LLM_API_KEY, LLM_MODEL


class RegexFilenameScraper:
    """
    Scraper that extracts comic metadata directly from the archive filename using Regex.
    """

    def __init__(self) -> None:
        """Initialize with pre-compiled regex patterns."""
        self.re_volume = re.compile(r'[vV]ol(ume)?\.?\s?(\d+)|[vV](\d+)')
        self.re_number = re.compile(r'#(\d+)|(?<=\s)(\d+)(?=\s|\.|\)|$)|(?<=\w)(\d+)(?=\s|\.|\)|$)') 
        self.re_year = re.compile(r'\((\d{4})\)')

    def search(self, comic: ComicInfo) -> ComicInfo:
        if not comic.path:
            return comic
        
        filename = os.path.basename(comic.path)
        basename = os.path.splitext(filename)[0]
        
        # Extract Year
        match_year = self.re_year.search(basename)
        if match_year:
            comic.Year = int(match_year.group(1))
            basename = basename.replace(match_year.group(0), "")
            
        # Extract Volume
        match_volume = self.re_volume.search(basename)
        if match_volume:
            vol_str = match_volume.group(2) or match_volume.group(3)
            comic.Volume = int(vol_str)
            basename = basename.replace(match_volume.group(0), "")
            
        # Extract Number
        match_number = self.re_number.search(basename)
        if match_number:
            num_str = match_number.group(1) or match_number.group(2) or match_number.group(3)
            comic.Number = num_str
            basename = basename.replace(match_number.group(0), "")
            
        # Clean up Series
        series = re.sub(r'\[.*?\]|\(.*?\)', '', basename).strip()
        series = re.sub(r'\s+', ' ', series)
        series = series.rstrip(" #-_").strip()
        
        comic.Series = series
        
        return comic


class OldSchoolFilenameScraper:
    """
    Scraper that extracts metadata by comparing filenames in the same directory.
    """

    def search(self, comic: ComicInfo) -> ComicInfo:
        if not comic.path or not os.path.isfile(comic.path):
            return comic

        directory = os.path.dirname(comic.path)
        filename = os.path.basename(comic.path)
        
        # Get all comic files in the same directory
        extensions = {'.cbz', '.cbr', '.cb7', '.zip', '.rar'}
        all_files = sorted([
            f for f in os.listdir(directory)
            if os.path.splitext(f)[1].lower() in extensions
        ])

        if len(all_files) < 2:
            # Fallback to Regex if only one file
            return RegexFilenameScraper().search(comic)

        # Find common prefix and suffix
        prefix = self._get_common_prefix(all_files)
        suffix = self._get_common_suffix(all_files)

        # Refine prefix to avoid including part of the number
        while prefix and prefix[-1].isdigit():
            prefix = prefix[:-1]

        # Extract variable part for the current file
        variable = filename[len(prefix):len(filename)-len(suffix)]
        
        # Identify Number/Volume from variable part
        variable = variable.lstrip(" #-_")
        num_match = re.search(r'(\d+)', variable)
        if num_match:
            comic.Number = num_match.group(1)
        else:
            comic.Number = variable.strip()

        # Series is the prefix, cleaned up
        series = prefix.strip()
        series = re.sub(r'(\s+[vV](ol(ume)?\.?)?|#+)$', '', series, flags=re.IGNORECASE)
        series = series.rstrip(" #-_").strip()
        series = re.sub(r'^\[.*?\]', '', series).strip()
        
        comic.Series = series
        
        # Year
        year_match = re.search(r'\((\d{4})\)', filename)
        if year_match:
            comic.Year = int(year_match.group(1))

        return comic

    def _get_common_prefix(self, strings: List[str]) -> str:
        if not strings: return ""
        s1 = min(strings)
        s2 = max(strings)
        for i, c in enumerate(s1):
            if i >= len(s2) or c != s2[i]:
                return s1[:i]
        return s1

    def _get_common_suffix(self, strings: List[str]) -> str:
        if not strings: return ""
        reversed_strings = [s[::-1] for s in strings]
        prefix = self._get_common_prefix(reversed_strings)
        return prefix[::-1]


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
            # Fallback to Regex if no API key or path
            return RegexFilenameScraper().search(comic)

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
            # Fallback to Regex on error
            print(f"LLM Scraper error: {e}")
            return RegexFilenameScraper().search(comic)

        return comic


# Backward compatibility
FilenameScraper = RegexFilenameScraper
