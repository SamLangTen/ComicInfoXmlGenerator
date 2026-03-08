# Track Specification: Fix Books.com.tw Scraper

## Overview
The goal of this track is to fix the Books.com.tw (`books_scraper.py`) metadata scraper. Currently, it fails to correctly identify and parse HTML from both search result pages and individual book detail pages on the `books.com.tw` website.

## Functional Requirements
- **Search Result Parsing:** Update the logic to reliably identify and extract the link to the most relevant book from Books.com.tw search results.
- **Detail Page Metadata Extraction:** Fix HTML parsing of the detail page to extract:
    - **Basic Info:** Title, Series name, and Volume/Issue number.
    - **Creation & Pub Info:** Author(s), Artist(s), Publisher, and Release Date.
    - **Content Details:** Genres, Tags, and Description.
- **Protocol Compliance:** Ensure the scraper continues to adhere to the `ScraperProtocol` defined in `src/scraper/protocol.py`.
- **Error Handling:** Implement robust handling for network failures (timeouts, 404s) and unexpected HTML structure changes.

## Acceptance Criteria
- **Successful Search:** The scraper can take a title string and successfully find the corresponding book URL on Books.com.tw.
- **Accurate Extraction:** All specified metadata fields (Basic, Creation/Pub, and Content) are correctly populated for a variety of test cases (e.g., single volumes and series).
- **Test Suite:** Comprehensive unit tests are implemented using mocked HTML responses for both search results and detail pages.
- **Zero Hallucinations:** The scraper only extracts information found on the page, with no "best-guess" defaults for missing fields.

## Out of Scope
- Implementing support for additional online metadata sources.
- Major changes to the general scraper architecture or UI.
- Handling of "Out of Stock" or "Pre-order" items if their page structure is radically different (unless they are the only available source).
