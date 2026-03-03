from .protocol import Scraper
from .local_scraper import LocalFilenameScraper
from .llm_scraper import LlmFilenameScraper

# Backward compatibility aliases
RegexFilenameScraper = LocalFilenameScraper
OldSchoolFilenameScraper = LocalFilenameScraper
FilenameScraper = LocalFilenameScraper

__all__ = [
    "Scraper", 
    "LocalFilenameScraper", 
    "LlmFilenameScraper", 
    "RegexFilenameScraper", 
    "OldSchoolFilenameScraper", 
    "FilenameScraper"
]
