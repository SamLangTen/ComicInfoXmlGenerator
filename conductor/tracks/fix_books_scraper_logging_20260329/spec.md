# Specification: `fix_books_scraper_logging_20260329`

## Overview
The Books.com.tw (博客来) scraper is currently failing to retrieve metadata ("no data" returned). This track focuses on identifying the cause of this failure, fixing it, and enhancing the scraper's logging to ensure better observability through both the Web UI and the main application log.

## Functional Requirements
- **Scraper Investigation**: Analyze the `books_scraper.py` to determine why it's failing to extract data.
- **Bug Fix**: Apply necessary changes to the scraping logic (e.g., regex, selectors, or request headers) to restore functionality.
- **Enhanced Logging**:
    - Integrate scraper-specific logging into the existing real-time logging system (WebSockets).
    - Ensure all key steps (request URL, response status, extraction results) are logged at the **Standard (Info)** level.
    - Log detailed error messages if data extraction fails.
- **Main Log Integration**: Ensure these logs are also persisted in the main application log file.

## Non-Functional Requirements
- **Maintainability**: Logging should be implemented using a consistent pattern that can be easily applied to other scrapers.
- **Robustness**: The fix should ideally handle minor future changes in the target website's structure.

## Acceptance Criteria
1.  **Functional Scraper**: The Books.com.tw scraper correctly retrieves metadata (Title, Series, Author, etc.) for a valid test book.
2.  **Real-time Observability**: Scraper logs are visible in the Web UI's live log stream during a scan or scrape operation.
3.  **Auditability**: Corresponding log entries are found in the main application log file.
4.  **No Regression**: Existing functionality for other scrapers remains unaffected.

## Out of Scope
- Adding new scrapers for other websites.
- Redesigning the entire UI's logging component.
- Implementing a full-blown debugger for scrapers.
