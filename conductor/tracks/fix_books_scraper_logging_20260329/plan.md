# Implementation Plan - Books.com.tw Scraper Fix & Logging Enhancement

Investigate and fix the Books.com.tw scraper failure ("no data") and enhance real-time logging for better observability in the Web UI.

## Phase 1: Investigation & Reproduction
- [ ] Task: Create a reproduction script `test/reproduce_books_failure.py` to confirm "no data" issue.
- [ ] Task: Run the reproduction script and analyze the HTML/Response from Books.com.tw.
- [ ] Task: Identify if selectors have changed or if the site is blocking requests (403/429).
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Investigation & Reproduction' (Protocol in workflow.md)

## Phase 2: Scraper Logic Fix
- [ ] Task: Update `src/scraper/books_scraper.py` with corrected selectors or request handling.
- [ ] Task: Verify the fix using the reproduction script.
- [ ] Task: Add/Update unit tests in `test/test_books_scraper_fixed.py` to ensure long-term stability.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Scraper Logic Fix' (Protocol in workflow.md)

## Phase 3: Real-time Logging Enhancement
- [ ] Task: Modify `src/task_manager.py`'s `scrape_task_handler` to support incremental log broadcasting if possible.
- [ ] Task: Add more granular `_log` calls in `BooksScraper.search` and `_extract_details`.
- [ ] Task: Implement a "Debug" mode in `BooksScraper` to log key HTML fragments when extraction fails.
- [ ] Task: Ensure logs are properly formatted and include timestamps or clear step markers.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Real-time Logging Enhancement' (Protocol in workflow.md)

## Phase 4: Integration & Verification
- [ ] Task: Run a full end-to-end test using the Web UI to verify real-time log streaming.
- [ ] Task: Verify that logs are also appearing in the main application log file.
- [ ] Task: Perform a regression test on other scrapers (Local, LLM).
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Integration & Verification' (Protocol in workflow.md)
