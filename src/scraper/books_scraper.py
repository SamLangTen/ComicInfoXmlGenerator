import httpx
import re
from typing import List, Optional, Callable
from bs4 import BeautifulSoup
from src.comic_info import ComicInfo

class BooksScraper:
    """
    Metadata scraper for Books.com.tw (博客來).
    """

    def __init__(self) -> None:
        self.base_url = "https://www.books.com.tw"
        self.search_url = "https://search.books.com.tw/search/query/key/{}/cat/all/v/1"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }

    def search(self, comic: ComicInfo, log_callback: Optional[Callable[[str], None]] = None) -> ComicInfo:
        # Use Title or Series as search keyword
        query = comic.Title or comic.Series
        if not query:
            if log_callback: log_callback("[Books.tw] Skipping: No title/series available to search.")
            return comic

        # Determine which parser to use
        parser = "lxml"
        try:
            import lxml
        except ImportError:
            parser = "html.parser"
            if log_callback: log_callback("[Books.tw] Warning: lxml not found, falling back to html.parser")

        if log_callback: log_callback(f"[Books.tw] Starting search for query: '{query}' using {parser}")

        try:
            with httpx.Client(headers=self.headers, follow_redirects=True, timeout=15.0) as client:
                # 1. Search for the book
                url = self.search_url.format(query)
                if log_callback: log_callback(f"[Books.tw] GET Request: {url}")
                
                resp = client.get(url)
                if log_callback: log_callback(f"[Books.tw] Response Status: {resp.status_code}")
                
                if resp.status_code != 200:
                    if log_callback: log_callback(f"[Books.tw] Error: Search failed with status {resp.status_code}")
                    return comic

                soup = BeautifulSoup(resp.text, parser)
                
                # Enhanced selector for search results
                result_link = None
                # Method A: Standard list view
                result_link = soup.select_one(".table-searchlist h4 a")
                # Method B: Grid view or alternate mod
                if not result_link:
                    result_link = soup.select_one(".mod_type02_m001 h4 a")
                
                if not result_link:
                    if log_callback: log_callback(f"[Books.tw] No results found in HTML for '{query}'")
                    return comic

                detail_url = result_link.get("href")
                if detail_url.startswith("//"):
                    detail_url = "https:" + detail_url
                elif not detail_url.startswith("http"):
                    detail_url = self.base_url + detail_url

                if log_callback: log_callback(f"[Books.tw] Found match: '{result_link.get_text(strip=True)}'")
                if log_callback: log_callback(f"[Books.tw] GET Detail Page: {detail_url}")

                # 2. Get details
                detail_resp = client.get(detail_url)
                if log_callback: log_callback(f"[Books.tw] Detail Response Status: {detail_resp.status_code}")
                
                if detail_resp.status_code == 200:
                    self._extract_details(detail_resp.text, comic, parser, log_callback)
                else:
                    if log_callback: log_callback(f"[Books.tw] Error: Failed to load detail page ({detail_resp.status_code})")

        except Exception as e:
            if log_callback: log_callback(f"[Books.tw] Exception occurred: {str(e)}")

        return comic

    def _extract_details(self, html: str, comic: ComicInfo, parser: str, log_callback: Optional[Callable[[str], None]] = None):
        soup = BeautifulSoup(html, parser)

        # Title
        title_elem = soup.select_one(".mod_type02_m001 h1") or soup.select_one("h1")
        if title_elem:
            title_text = title_elem.get_text(strip=True)
            if log_callback: log_callback(f"[Books.tw] Extracting data for: {title_text}")
            if not comic.Title: comic.Title = title_text
            
            vol_match = re.search(r'(\d+)$', title_text)
            if vol_match and comic.Volume == -1:
                comic.Volume = int(vol_match.group(1))
                if log_callback: log_callback(f"[Books.tw] Inferred Volume: {comic.Volume}")

        # Author/Publisher/Date
        info_block = soup.select_one(".type02_p003")
        if info_block:
            # Author
            author_link = info_block.select_one('a[href*="adv_author"]')
            if author_link:
                author = author_link.get_text(strip=True)
                comic.Writer = author
                if log_callback: log_callback(f"[Books.tw] Author: {author}")

            # Publisher
            pub_link = info_block.select_one('a[href*="pubid"]')
            if pub_link:
                pub = pub_link.get_text(strip=True)
                comic.Publisher = pub
                if log_callback: log_callback(f"[Books.tw] Publisher: {pub}")

            # Date
            text = info_block.get_text()
            date_match = re.search(r'出版日期：(\d{4})/(\d{2})/(\d{2})', text)
            if date_match:
                comic.Year = int(date_match.group(1))
                comic.Month = int(date_match.group(2))
                comic.Day = int(date_match.group(3))
                if log_callback: log_callback(f"[Books.tw] Date: {comic.Year}/{comic.Month}/{comic.Day}")

        # Summary
        summary_elem = soup.select_one(".content") or soup.select_one(".mod_type02_m012")
        if summary_elem:
            comic.Summary = summary_elem.get_text(strip=True)
            if log_callback: log_callback(f"[Books.tw] Summary: {comic.Summary[:50]}...")

        if log_callback: log_callback(f"[Books.tw] Successfully updated metadata.")

    def search_batch(self, comics: List[ComicInfo], log_callback: Optional[Callable[[str], None]] = None) -> List[ComicInfo]:
        for comic in comics:
            self.search(comic, log_callback=log_callback)
        return comics
