import re
import os
from typing import List, Optional, Callable
from src.comic_info import ComicInfo

class LocalFilenameScraper:
    """
    Consolidated scraper that extracts comic metadata from filenames.
    """

    def __init__(self) -> None:
        self.re_volume = re.compile(r'[vV]ol(ume)?\.?\s?(\d+)|[vV](\d+)')
        self.re_number = re.compile(r'#(\d+)|(?<=\s)(\d+)(?=\s|\.|\)|$)|(?<=\D)(\d+)(?=\D|$)') 
        self.re_year = re.compile(r'\((\d{4})\)')

    def search(self, comic: ComicInfo, log_callback: Optional[Callable[[str], None]] = None) -> ComicInfo:
        if not comic.path or not os.path.isfile(comic.path):
            return comic

        directory = os.path.dirname(comic.path)
        filename = os.path.basename(comic.path)
        
        # 1. Try Directory-Based Inference
        extensions = {'.cbz', '.cbr', '.cb7', '.zip', '.rar'}
        all_files = sorted([
            f for f in os.listdir(directory)
            if os.path.splitext(f)[1].lower() in extensions
        ])

        if len(all_files) >= 2:
            prefix = self._get_common_prefix(all_files)
            suffix = self._get_common_suffix(all_files)
            temp_prefix = prefix
            while temp_prefix and temp_prefix[-1].isdigit():
                temp_prefix = temp_prefix[:-1]

            variable = filename[len(temp_prefix):len(filename)-len(suffix)]
            variable = variable.lstrip(" #-_")
            num_match = re.search(r'(\d+)', variable)
            if num_match: comic.Number = num_match.group(1)
            else: comic.Number = variable.strip()

            series = temp_prefix.strip()
            series = re.sub(r'(\s+[vV](ol(ume)?\.?)?|#+)$', '', series, flags=re.IGNORECASE)
            series = series.rstrip(" #-_").strip()
            series = re.sub(r'^\[.*?\]', '', series).strip()
            
            if series:
                comic.Series = series
                year_match = self.re_year.search(filename)
                if year_match: comic.Year = int(year_match.group(1))
                return comic

        # 2. Fallback to Regex-Only (Simple sequential)
        basename = os.path.splitext(filename)[0]
        
        # Extract Year
        my = self.re_year.search(basename)
        if my: comic.Year = int(my.group(1))
        
        # Extract Volume
        mv = self.re_volume.search(basename)
        if mv: comic.Volume = int(mv.group(2) or mv.group(3))
        
        # Extract Number
        mn = self.re_number.search(basename)
        if mn: comic.Number = mn.group(1) or mn.group(2) or mn.group(3)

        # Simple Series extraction: take everything before the first number or tag
        # We look for the first occurrence of volume marker, issue marker, or year
        potential_splits = []
        if my: potential_splits.append(my.start())
        if mv: potential_splits.append(mv.start())
        if mn: potential_splits.append(mn.start())
        
        # Also look for bracket/parenthesis tags
        bracket = re.search(r'[\[\(]', basename)
        if bracket: potential_splits.append(bracket.start())
        
        split_pos = min(potential_splits) if potential_splits else len(basename)
        series = basename[:split_pos].strip()
        
        # If the result is empty (e.g. filename starts with number), fallback
        if not series:
            series = re.sub(r'\[.*?\]|\(.*?\)', '', basename).strip()
            series = re.sub(r'#?\d+', '', series).strip()
            
        comic.Series = series.strip(" #-_")
        
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
