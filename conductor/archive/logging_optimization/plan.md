# Implementation Plan: Logging Optimization [checkpoint: 2f3226d]

## Phase 1: Protocol and Scraper Refactor
- [x] Update `Scraper` protocol in `src/scraper/protocol.py` [5124810]
- [x] Update `LocalFilenameScraper` signature in `src/scraper/local_scraper.py` [5124810]
- [x] Implement verbose logging in `LlmFilenameScraper.search_batch` [5124810]

## Phase 2: GUI Integration
- [x] Create a thread-safe log dispatcher in `gui/app.py` [f202e3c]
- [x] Inject log callback into scraper calls [f202e3c]

## Phase 3: Verification
- [x] Verify logs appear in terminal when running GUI [f202e3c]
- [x] Verify logs appear in GUI `log_textbox` when running LLM [f202e3c]
- [x] Final verification and checkpoint [f202e3c]
