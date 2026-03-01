import re
import os
from src.comic_info import ComicInfo


class FilenameScraper:
    """
    Scraper that extracts comic metadata directly from the archive filename.
    
    This scraper uses regular expressions to parse common patterns in comic 
    filenames such as series name, volume number, issue number, and publication year.
    """

    def __init__(self) -> None:
        """Initialize the FilenameScraper with pre-compiled regex patterns."""
        # Regex patterns
        self.re_volume = re.compile(r'[vV]ol(ume)?\.?\s?(\d+)|[vV](\d+)')
        self.re_number = re.compile(r'#(\d+)|(?<=\s)(\d+)$') # matches #01 or standalone number at the end
        self.re_year = re.compile(r'\((\d{4})\)')

    def search(self, comic: ComicInfo) -> ComicInfo:
        """
        Extract metadata from the filename of the provided ComicInfo object.
        
        Args:
            comic: The ComicInfo object containing the file path to parse.
            
        Returns:
            The ComicInfo object updated with extracted metadata.
        """
        if not comic.path:
            return comic
        
        filename = os.path.basename(comic.path)
        # Remove extension
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
            # Remove volume part from basename
            basename = basename.replace(match_volume.group(0), "")
            
        # Extract Number
        match_number = self.re_number.search(basename)
        if match_number:
            num_str = match_number.group(1) or match_number.group(2)
            comic.Number = num_str
            # Remove number part from basename
            basename = basename.replace(match_number.group(0), "")
            
        # Extract Year (again for removal)
        match_year = self.re_year.search(basename)
        if match_year:
             basename = basename.replace(match_year.group(0), "")
             
        # What's left is Series (roughly)
        # Clean up brackets and extra spaces
        series = re.sub(r'\[.*?\]|\(.*?\)', '', basename).strip()
        series = re.sub(r'\s+', ' ', series)
        
        # Remove trailing junk from series (e.g. empty brackets)
        series = series.rstrip(" #").strip()
        
        comic.Series = series
        
        return comic
