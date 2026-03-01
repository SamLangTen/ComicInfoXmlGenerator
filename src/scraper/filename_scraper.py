import re
import os
from typing import List
from src.comic_info import ComicInfo


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
        # e.g., if files are "Comic 01.cbz", "Comic 02.cbz", prefix is "Comic 0"
        # We want prefix to be "Comic " and number to be "01", "02"
        while prefix and prefix[-1].isdigit():
            prefix = prefix[:-1]

        # Extract variable part for the current file
        # current_file = prefix + variable + suffix
        variable = filename[len(prefix):len(filename)-len(suffix)]
        
        # Identify Number/Volume from variable part
        # Clean up common separators from variable start
        variable = variable.lstrip(" #-_")
        num_match = re.search(r'(\d+)', variable)
        if num_match:
            comic.Number = num_match.group(1)
        else:
            # Fallback to the whole variable if no digits found
            comic.Number = variable.strip()

        # Series is the prefix, cleaned up
        series = prefix.strip()
        # Clean up common separators at the end of series
        # Remove trailing v, vol, volume, # etc.
        series = re.sub(r'(\s+[vV](ol(ume)?\.?)?|#+)$', '', series, flags=re.IGNORECASE)
        series = series.rstrip(" #-_").strip()
        # Also remove group tags like [ScanGroup]
        series = re.sub(r'^\[.*?\]', '', series).strip()
        
        comic.Series = series
        
        # Year might still be in the suffix or prefix, or somewhere else.
        # Use Regex for Year as it's usually (2024)
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


# Backward compatibility
FilenameScraper = RegexFilenameScraper
