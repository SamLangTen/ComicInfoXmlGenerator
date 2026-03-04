# Implementation Plan: Logging Optimization

## Phase 1: Protocol and Scraper Refactor
- [ ] Update `Scraper` protocol in `src/scraper/protocol.py` [ ]
- [ ] Update `LocalFilenameScraper` signature in `src/scraper/local_scraper.py` [ ]
- [ ] Implement verbose logging in `LlmFilenameScraper.search_batch` [ ]

## Phase 2: GUI Integration
- [ ] Create a thread-safe log dispatcher in `gui/app.py` [ ]
- [ ] Inject log callback into scraper calls [ ]

## Phase 3: Verification
- [ ] Verify logs appear in terminal when running GUI [ ]
- [ ] Verify logs appear in GUI `log_textbox` when running LLM [ ]
- [ ] Final verification and checkpoint [ ]
