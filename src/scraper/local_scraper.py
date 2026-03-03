import re
import os
from typing import List
from src.comic_info import ComicInfo

class LocalFilenameScraper:
    """
    Consolidated scraper that extracts comic metadata from filenames.
    It prefers directory-context-based inference (Common Prefix/Suffix)
    and falls back to Regex pattern matching if only one file exists.
    """

    def __init__(self) -> None:
        # Regex patterns for fallback
        self.re_volume = re.compile(r'[vV]ol(ume)?\.?\s?(\d+)|[vV](\d+)')
        self.re_number = re.compile(r'#(\d+)|(?<=\s)(\d+)(?=\s|\.|\)|$)|(?<=\w)(\d+)(?=\s|\.|\)|$)') 
        self.re_year = re.compile(r'\((\d{4})\)')

    def search(self, comic: ComicInfo) -> ComicInfo:
        if not comic.path or not os.path.isfile(comic.path):
            return comic

        directory = os.path.dirname(comic.path)
        filename = os.path.basename(comic.path)
        
        # 1. Try Directory-Based Inference (OldSchool logic)
        extensions = {'.cbz', '.cbr', '.cb7', '.zip', '.rar'}
        all_files = sorted([
            f for f in os.listdir(directory)
            if os.path.splitext(f)[1].lower() in extensions
        ])

        if len(all_files) >= 2:
            prefix = self._get_common_prefix(all_files)
            suffix = self._get_common_suffix(all_files)
            
            # Refine prefix to separate number
            while prefix and prefix[-1].isdigit():
                prefix = prefix[:-1]

            variable = filename[len(prefix):len(filename)-len(suffix)]
            variable = variable.lstrip(" #-_")
            
            num_match = re.search(r'(\d+)', variable)
            if num_match:
                comic.Number = num_match.group(1)
            else:
                comic.Number = variable.strip()

            series = prefix.strip()
            # Clean up trailing separators/volume markers
            series = re.sub(r'(\s+[vV](ol(ume)?\.?)?|#+)$', '', series, flags=re.IGNORECASE)
            series = series.rstrip(" #-_").strip()
            series = re.sub(r'^\[.*?\]', '', series).strip()
            comic.Series = series

            # Year usually stays in basename or suffix
            year_match = self.re_year.search(filename)
            if year_match:
                comic.Year = int(year_match.group(1))
            
            # If we successfully got a series, we are happy
            if comic.Series:
                return comic

        # 2. Fallback to Regex-Only (Regex logic)
        basename = os.path.splitext(filename)[0]
        
        match_year = self.re_year.search(basename)
        if match_year:
            comic.Year = int(match_year.group(1))
            basename = basename.replace(match_year.group(0), "")
            
        match_volume = self.re_volume.search(basename)
        if match_volume:
            vol_str = match_volume.group(2) or match_volume.group(3)
            comic.Volume = int(vol_str)
            basename = basename.replace(match_volume.group(0), "")
            
        match_number = self.re_number.search(basename)
        if match_number:
            num_str = match_number.group(1) or match_number.group(2) or match_number.group(3)
            comic.Number = num_str
            basename = basename.replace(match_number.group(0), "")
            
        series = re.sub(r'\[.*?\]|\(.*?\)', '', basename).strip()
        series = re.sub(r'\s+', ' ', series)
        series = series.rstrip(" #-_").strip()
        comic.Series = series
        
        return comic

    def _get_common_prefix(self, strings: List[str]) -> str:
        if not strings: return ""
        s1 = min(strings); s2 = max(strings)
        for i, c in enumerate(s1):
            if i >= len(s2) or c != s2[i]: return s1[:i]
        return s1

    def _get_common_suffix(self, strings: List[str]) -> str:
        if not strings: return ""
        reversed_strings = [s[::-1] for s in strings]
        prefix = self._get_common_prefix(reversed_strings)
        return prefix[::-1]
