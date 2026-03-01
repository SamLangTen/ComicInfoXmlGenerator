# Implementation Plan: Advanced Scrapers [checkpoint: fe96ad2]

## Phase 1: Setup and Infrastructure
- [x] Update `tech-stack.md` and create `requirements.txt` [7f5ab32]
- [x] Configure environment variable loading (e.g., `.env`) [6942d08]

## Phase 2: OldSchoolFilenameScraper
- [x] Implement `OldSchoolFilenameScraper` logic in `src/scraper/filename_scraper.py` [ab1f39f]
- [x] Add unit tests for `OldSchoolFilenameScraper` with directory mocking [ab1f39f]
- [x] Verify functionality with various naming patterns [ab1f39f]

## Phase 3: LlmFilenameScraper
- [x] Implement `LlmFilenameScraper` using `httpx` [17a0ac1]
- [x] Add unit tests for `LlmFilenameScraper` with API mocking [17a0ac1]
- [x] Implement robust error handling for API failures [17a0ac1]

## Phase 4: Integration and Cleanup
- [x] Update `src/scraper/__init__.py` to export new scrapers [ab1f39f, 17a0ac1]
- [x] Update `test/test_filename_scraper.py` to cover all scrapers [f34b45d]
- [x] Final verification and checkpoint [f34b45d]
