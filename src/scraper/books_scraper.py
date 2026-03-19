import httpx
import re
import logging
from typing import List, Optional, Callable
from bs4 import BeautifulSoup
from urllib.parse import quote
from src.comic_info import ComicInfo

logger = logging.getLogger(__name__)

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

    def _log(self, message: str, log_callback: Optional[Callable[[str], None]] = None):
        logger.info(message)
        if log_callback:
            log_callback(message)

    def search(self, comic: ComicInfo, log_callback: Optional[Callable[[str], None]] = None) -> ComicInfo:
        # Use Title or Series as search keyword
        query = comic.Title or comic.Series
        if not query:
            self._log("[Books.tw] Skipping: No title/series available to search.", log_callback)
            return comic

        # Determine which parser to use
        parser = "lxml"
        try:
            import lxml
        except ImportError:
            parser = "html.parser"
            self._log("[Books.tw] Warning: lxml not found, falling back to html.parser", log_callback)

        self._log(f"[Books.tw] Starting search for query: '{query}' using {parser}", log_callback)

        try:
            # Use a session-like approach with httpx.Client to maintain cookies if any
            with httpx.Client(headers=self.headers, follow_redirects=True, timeout=15.0) as client:
                # 1. Search for the book
                url = self.search_url.format(quote(query))
                self._log(f"[Books.tw] GET Request: {url}", log_callback)
                
                resp = client.get(url)
                self._log(f"[Books.tw] Response Status: {resp.status_code}", log_callback)
                
                if resp.status_code != 200:
                    self._log(f"[Books.tw] Error: Search failed with status {resp.status_code}", log_callback)
                    return comic

                soup = BeautifulSoup(resp.text, parser)
                
                # Enhanced selector for search results
                result_link = None
                # New method: find the first result in the list
                result_item = soup.select_one(".table-td")
                if result_item:
                    result_link = result_item.select_one("h4 a")
                
                # Fallback to old methods
                if not result_link:
                    result_link = soup.select_one(".table-searchlist h4 a") or soup.select_one(".mod_type02_m001 h4 a")
                
                if not result_link:
                    self._log(f"[Books.tw] No results found in HTML for '{query}'", log_callback)
                    return comic

                detail_url = result_link.get("href")
                if detail_url.startswith("//"):
                    detail_url = "https:" + detail_url
                elif not detail_url.startswith("http"):
                    detail_url = self.base_url + detail_url

                self._log(f"[Books.tw] Found match: '{result_link.get_text(strip=True)}'", log_callback)
                
                # Update headers with Referer for the detail page request
                detail_headers = self.headers.copy()
                detail_headers["Referer"] = url
                
                self._log(f"[Books.tw] GET Detail Page: {detail_url}", log_callback)

                # 2. Get details
                detail_resp = client.get(detail_url, headers=detail_headers)
                self._log(f"[Books.tw] Detail Response Status: {detail_resp.status_code}", log_callback)
                
                if detail_resp.status_code == 200:
                    self._extract_details(detail_resp.text, comic, parser, log_callback)
                elif detail_resp.status_code == 403:
                    self._log(f"[Books.tw] Error: Access Forbidden (403). Books.com.tw might be blocking the request.", log_callback)
                else:
                    self._log(f"[Books.tw] Error: Failed to load detail page ({detail_resp.status_code})", log_callback)

        except Exception as e:
            self._log(f"[Books.tw] Exception occurred: {str(e)}", log_callback)

        return comic

    def _extract_details(self, html: str, comic: ComicInfo, parser: str, log_callback: Optional[Callable[[str], None]] = None):
        soup = BeautifulSoup(html, parser)

        # 1. Try JSON-LD first (Robust)
        import json
        json_ld = soup.find("script", type="application/ld+json")
        if json_ld:
            try:
                data = json.loads(json_ld.string)
                if data.get("@type") == "Book":
                    self._log("[Books.tw] Using JSON-LD data.", log_callback)
                    comic.Title = data.get("name", comic.Title)
                    
                    authors = data.get("author", [])
                    if isinstance(authors, list) and authors:
                        comic.Writer = authors[0].get("name", comic.Writer)
                    elif isinstance(authors, dict):
                        comic.Writer = authors.get("name", comic.Writer)
                    
                    publisher = data.get("publisher")
                    if isinstance(publisher, list) and publisher:
                        comic.Publisher = publisher[0].get("name", comic.Publisher)
                    elif isinstance(publisher, dict):
                        comic.Publisher = publisher.get("name", comic.Publisher)
                    
                    date_pub = data.get("datePublished")
                    if date_pub:
                        date_match = re.search(r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})', date_pub)
                        if date_match:
                            comic.Year = int(date_match.group(1))
                            comic.Month = int(date_match.group(2))
                            comic.Day = int(date_match.group(3))
            except Exception as e:
                self._log(f"[Books.tw] JSON-LD error: {str(e)}", log_callback)

        # 2. HTML Fallback / Supplement
        # Title & Volume (if not set or needs refining)
        title_elem = soup.select_one(".mod_type02_m001 h1") or soup.select_one("h1")
        if title_elem:
            title_text = title_elem.get_text(strip=True)
            comic.Title = title_text # Update Title from detail page
            
            # Extract volume from title if not already set
            if comic.Volume == -1:
                vol_match = re.search(r'(\d+)(?:\s*\(.*\))?$', title_text)
                if vol_match:
                    comic.Volume = int(vol_match.group(1))

        # Author/Publisher/Date (Fallback)
        if not comic.Writer or not comic.Publisher or comic.Year == -1:
            info_block = soup.select_one(".type02_p003")
            if info_block:
                if not comic.Writer:
                    author_link = info_block.select_one('a[href*="adv_author"]')
                    if author_link:
                        comic.Writer = author_link.get_text(strip=True)

                if not comic.Publisher:
                    pub_link = info_block.select_one('a[href*="pubid"]')
                    if pub_link:
                        comic.Publisher = pub_link.get_text(strip=True)

                if comic.Year == -1:
                    text = info_block.get_text()
                    date_match = re.search(r'出版日期：(\d{4})/(\d{2})/(\d{2})', text)
                    if date_match:
                        comic.Year = int(date_match.group(1))
                        comic.Month = int(date_match.group(2))
                        comic.Day = int(date_match.group(3))

        # Summary
        summary_elem = soup.select_one(".mod_b.type02_m057 .content") or \
                       soup.select_one(".mod_type02_m012 .content") or \
                       soup.select_one(".content")
        if summary_elem:
            comic.Summary = summary_elem.get_text(strip=True)

        # Genre/Tags
        sort_block = soup.select_one(".sort")
        if sort_block:
            categories = [a.get_text(strip=True) for a in sort_block.select("a")]
            if categories:
                comic.Genre = ",".join(categories)

        self._log(f"[Books.tw] Metadata extraction complete.", log_callback)

    def search_batch(self, comics: List[ComicInfo], log_callback: Optional[Callable[[str], None]] = None) -> List[ComicInfo]:
        for comic in comics:
            self.search(comic, log_callback=log_callback)
        return comics
