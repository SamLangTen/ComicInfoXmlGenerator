# Implementation Plan: Scraper Consolidation

## Phase 1: Code Migration
- [ ] Create `src/scraper/local_scraper.py` with merged logic [ ]
- [ ] Create `src/scraper/llm_scraper.py` with LLM logic [ ]
- [ ] Remove redundant `src/scraper/filename_scraper.py` [ ]

## Phase 2: API and Integration
- [ ] Update `src/scraper/__init__.py` with new exports [ ]
- [ ] Update imports in `src/cixg.py` [ ]
- [ ] Update imports in `gui/app.py` [ ]

## Phase 3: Testing and Cleanup
- [ ] Refactor `test/test_filename_scraper.py` to target new classes [ ]
- [ ] Verify all 20 existing tests pass [ ]
- [ ] Final verification and checkpoint [ ]
