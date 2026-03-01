# Implementation Plan: Advanced Scrapers

## Phase 1: Setup and Infrastructure
- [x] Update `tech-stack.md` and create `requirements.txt` [7f5ab32]
- [x] Configure environment variable loading (e.g., `.env`) [6942d08]

## Phase 2: OldSchoolFilenameScraper
- [x] Implement `OldSchoolFilenameScraper` logic in `src/scraper/filename_scraper.py` [ab1f39f]
- [x] Add unit tests for `OldSchoolFilenameScraper` with directory mocking [ab1f39f]
- [x] Verify functionality with various naming patterns [ab1f39f]

## Phase 3: LlmFilenameScraper
- [~] Implement `LlmFilenameScraper` using `httpx` [ ]
- [ ] Add unit tests for `LlmFilenameScraper` with API mocking [ ]
- [ ] Implement robust error handling for API failures [ ]

## Phase 4: Integration and Cleanup
- [ ] Update `src/scraper/__init__.py` to export new scrapers [ ]
- [ ] Update `test/test_filename_scraper.py` to cover all scrapers [ ]
- [ ] Final verification and checkpoint [ ]
