from typing import Protocol, Optional
from src.comic_info import ComicInfo


class Scraper(Protocol):
    """
    Protocol for metadata scrapers.
    
    Any class that implements a search method accepting a ComicInfo object
    and returning a ComicInfo object satisfies this protocol.
    """

    def search(self, comic: ComicInfo) -> ComicInfo:
        """
        Search for metadata and update the ComicInfo object.
        
        Args:
            comic: The ComicInfo object to enrich with metadata.
            
        Returns:
            The enriched ComicInfo object.
        """
        ...
