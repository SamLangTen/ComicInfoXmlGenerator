# Implementation Plan: GUI Refinement

## Phase 1: Configuration Engine
- [x] Implement `src/config_manager.py` for persistent settings [b21e5e0]
- [x] Refactor `src/config.py` to use `ConfigManager` [b21e5e0]

## Phase 2: GUI Restructuring
- [x] Implement a Tabbed navigation or Sidebar switcher for "Editor" vs "Settings" [2c10dbe]
- [x] Build the "Settings" view with LLM and UI controls [2c10dbe]

## Phase 3: Theme Restoration
- [x] Re-enable `customtkinter` theme switching logic [146e421]
- [x] Fix macOS version error by conditionally applying theme settings [146e421]

## Phase 4: LLM Integration and Validation
- [x] Connect GUI settings to `LlmFilenameScraper` [0fa0886]
- [x] Add visual feedback for scraper execution and errors [0fa0886]

## Phase 5: Final Testing
- [x] Verify Light/Dark mode transitions [0fa0886]
- [x] Test settings persistence after restart [0fa0886]
- [x] Final verification and checkpoint [0fa0886]
