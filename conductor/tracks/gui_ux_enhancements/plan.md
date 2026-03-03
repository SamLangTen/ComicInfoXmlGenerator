# Implementation Plan: GUI UX Enhancements

## Phase 1: Logging and Preparation
- [ ] Update `LlmFilenameScraper` to log prompts to stdout [ ]
- [ ] Implement a `StatusBar` or generic progress indicator in `gui/app.py` [ ]

## Phase 2: Manual Scraper Control
- [ ] Add "Apply Scraper" button to the Editor tab [ ]
- [ ] Decouple file selection from automatic scraping [ ]

## Phase 3: Threading Integration
- [ ] Implement `run_background_task` helper in `App` class [ ]
- [ ] Wrap scraper logic in a background thread [ ]
- [ ] Ensure UI updates (form loading) happen on the main thread via `after` [ ]

## Phase 4: Final Testing
- [ ] Verify UI remains interactive during LLM calls [ ]
- [ ] Verify progress bar visibility during tasks [ ]
- [ ] Final verification and checkpoint [ ]
