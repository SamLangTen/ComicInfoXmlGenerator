import sys
import os
import asyncio

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.scraper.books_scraper import BooksScraper
from src.comic_info import ComicInfo

def log_callback(msg):
    print(f"LOG: {msg}")

def reproduce():
    scraper = BooksScraper()
    test_queries = [
        "葬送的芙莉蓮 1", 
        "海賊王 100", 
        "SPY×FAMILY 間諜家家酒 1",
        "UNKNOWN_BOOK_123456"
    ]
    
    failures = []
    for query in test_queries:
        comic = ComicInfo(Title=query)
        print(f"\n{'='*20}")
        print(f"Starting search for: {comic.Title}")
        result = scraper.search(comic, log_callback=log_callback)
        
        print("\n--- Final Metadata ---")
        print(f"Title: {result.Title}")
        print(f"Writer: {result.Writer}")
        print(f"Publisher: {result.Publisher}")
        
        if query == "UNKNOWN_BOOK_123456":
            continue
            
        if not result.Writer or not result.Publisher:
            print(f"\nFAILURE: Incomplete metadata for '{query}'.")
            failures.append(query)
        else:
            print(f"\nSUCCESS: Metadata extracted for '{query}'.")
            
    if failures:
        print(f"\nTotal failures: {len(failures)} ({', '.join(failures)})")
        sys.exit(1)
    else:
        print("\nAll tests PASSED.")
        sys.exit(0)

if __name__ == "__main__":
    reproduce()
