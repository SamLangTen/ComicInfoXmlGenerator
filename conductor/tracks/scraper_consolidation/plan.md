# Implementation Plan: Scraper Consolidation

## Phase 1: Code Migration
- [x] Create `src/scraper/local_scraper.py` with merged logic [b155616]
- [x] Create `src/scraper/llm_scraper.py` with LLM logic [b155616]
- [x] Remove redundant `src/scraper/filename_scraper.py` [b155616]

## Phase 2: API and Integration
- [x] Update `src/scraper/__init__.py` with new exports [22e71c5]
- [x] Update imports in `src/cixg.py` [22e71c5]
- [x] Update imports in `gui/app.py` [22e71c5]

## Phase 3: Testing and Cleanup
- [x] Refactor `test/test_filename_scraper.py` to target new classes [3ae5107]
- [~] Verify all 20 existing tests pass [ ]
- [ ] Final verification and checkpoint [ ]
