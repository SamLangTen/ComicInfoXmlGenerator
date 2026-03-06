# Implementation Plan: GUI UX Enhancements [checkpoint: 64f08ec]

## Phase 1: Logging and Preparation
- [x] Update `LlmFilenameScraper` to log prompts to stdout [ce60df8]
- [x] Implement a `StatusBar` or generic progress indicator in `gui/app.py` [ce60df8]

## Phase 2: Manual Scraper Control
- [x] Add "Apply Scraper" button to the Editor tab [ce60df8, d55f3c3]
- [x] Decouple file selection from automatic scraping [d55f3c3]

## Phase 3: Threading Integration
- [x] Implement `run_background_task` helper in `App` class [90a2018]
- [x] Wrap scraper logic in a background thread [90a2018]
- [x] Ensure UI updates (form loading) happen on the main thread via `after` [90a2018]

## Phase 4: Final Testing
- [x] Verify UI remains interactive during LLM calls [90a2018]
- [x] Verify progress bar visibility during tasks [90a2018]
- [x] Final verification and checkpoint [90a2018]
