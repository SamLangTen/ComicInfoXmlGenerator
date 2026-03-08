# Implementation Plan: Fix Books.com.tw Scraper

## Phase 1: Research and Setup
- [ ] Task: Gather current HTML structure for Books.com.tw search results and book detail pages.
- [ ] Task: Create a dedicated test file `test/test_books_scraper_fixed.py` and implement initial failing tests using mocked HTML responses.
- [ ] Task: Conductor - User Manual Verification 'Research and Setup' (Protocol in workflow.md)

## Phase 2: Fix Search Result Parsing
- [ ] Task: Update `BooksScraper._parse_search_results` to correctly extract the detail page URL from the modern Books.com.tw search page structure.
    - [ ] Write failing test for search result parsing.
    - [ ] Implement fix to pass the test.
    - [ ] Verify search result parsing logic.
- [ ] Task: Conductor - User Manual Verification 'Fix Search Result Parsing' (Protocol in workflow.md)

## Phase 3: Fix Detail Page Extraction
- [ ] Task: Update `BooksScraper._parse_detail_page` to extract "Basic Info" (Title, Series, Volume).
    - [ ] Write failing test for Basic Info extraction.
    - [ ] Implement extraction logic.
    - [ ] Verify Basic Info extraction.
- [ ] Task: Update `BooksScraper._parse_detail_page` to extract "Creation & Pub Info" (Author, Artist, Publisher, Release Date).
    - [ ] Write failing test for Creation & Pub Info extraction.
    - [ ] Implement extraction logic.
    - [ ] Verify Creation & Pub Info extraction.
- [ ] Task: Update `BooksScraper._parse_detail_page` to extract "Content Details" (Genre, Tags, Description).
    - [ ] Write failing test for Content Details extraction.
    - [ ] Implement extraction logic.
    - [ ] Verify Content Details extraction.
- [ ] Task: Conductor - User Manual Verification 'Fix Detail Page Extraction' (Protocol in workflow.md)

## Phase 4: Error Handling and Integration
- [ ] Task: Implement robust error handling for missing fields and unexpected HTML changes (e.g., using `Optional` and safe `get` methods).
    - [ ] Write failing tests for various error/edge cases.
    - [ ] Implement error handling logic.
- [ ] Task: Run full test suite for `BooksScraper` and verify coverage meets 80% threshold.
- [ ] Task: Conductor - User Manual Verification 'Error Handling and Integration' (Protocol in workflow.md)
