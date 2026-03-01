# Implementation Plan: Advanced Scrapers

## Phase 1: Setup and Infrastructure
- [x] Update `tech-stack.md` and create `requirements.txt` [7f5ab32]
- [~] Configure environment variable loading (e.g., `.env`) [ ]

## Phase 2: OldSchoolFilenameScraper
- [ ] Implement `OldSchoolFilenameScraper` logic in `src/scraper/filename_scraper.py` [ ]
- [ ] Add unit tests for `OldSchoolFilenameScraper` with directory mocking [ ]
- [ ] Verify functionality with various naming patterns [ ]

## Phase 3: LlmFilenameScraper
- [ ] Implement `LlmFilenameScraper` using `httpx` [ ]
- [ ] Add unit tests for `LlmFilenameScraper` with API mocking [ ]
- [ ] Implement robust error handling for API failures [ ]

## Phase 4: Integration and Cleanup
- [ ] Update `src/scraper/__init__.py` to export new scrapers [ ]
- [ ] Update `test/test_filename_scraper.py` to cover all scrapers [ ]
- [ ] Final verification and checkpoint [ ]
