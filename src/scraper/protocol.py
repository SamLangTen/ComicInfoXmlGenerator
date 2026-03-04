from typing import Protocol, Optional, List
from src.comic_info import ComicInfo


class Scraper(Protocol):
    """
    Protocol for metadata scrapers.
    """

    def search(self, comic: ComicInfo) -> ComicInfo:
        """Search for metadata for a single comic."""
        ...

    def search_batch(self, comics: List[ComicInfo]) -> List[ComicInfo]:
        """
        Search for metadata for multiple comics in a batch.
        Default implementation can just loop through search().
        """
        for comic in comics:
            self.search(comic)
        return comics
