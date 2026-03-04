from typing import Protocol, Optional, List, Callable
from src.comic_info import ComicInfo


class Scraper(Protocol):
    """
    Protocol for metadata scrapers.
    """

    def search(self, comic: ComicInfo, log_callback: Optional[Callable[[str], None]] = None) -> ComicInfo:
        """Search for metadata for a single comic."""
        ...

    def search_batch(self, comics: List[ComicInfo], log_callback: Optional[Callable[[str], None]] = None) -> List[ComicInfo]:
        """
        Search for metadata for multiple comics in a batch.
        """
        for comic in comics:
            self.search(comic, log_callback=log_callback)
        return comics
