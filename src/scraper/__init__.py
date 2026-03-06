from .protocol import Scraper
from .local_scraper import LocalFilenameScraper
from .llm_scraper import LlmFilenameScraper
from .books_scraper import BooksScraper

# Backward compatibility aliases
RegexFilenameScraper = LocalFilenameScraper
OldSchoolFilenameScraper = LocalFilenameScraper
FilenameScraper = LocalFilenameScraper

__all__ = [
    "Scraper", 
    "LocalFilenameScraper", 
    "LlmFilenameScraper", 
    "BooksScraper",
    "RegexFilenameScraper", 
    "OldSchoolFilenameScraper", 
    "FilenameScraper"
]
