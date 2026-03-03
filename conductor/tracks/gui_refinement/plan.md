# Implementation Plan: GUI Refinement

## Phase 1: Configuration Engine
- [ ] Implement `src/config_manager.py` for persistent settings [ ]
- [ ] Refactor `src/config.py` to use `ConfigManager` [ ]

## Phase 2: GUI Restructuring
- [ ] Implement a Tabbed navigation or Sidebar switcher for "Editor" vs "Settings" [ ]
- [ ] Build the "Settings" view with LLM and UI controls [ ]

## Phase 3: Theme Restoration
- [ ] Re-enable `customtkinter` theme switching logic [ ]
- [ ] Fix macOS version error by conditionally applying theme settings [ ]

## Phase 4: LLM Integration and Validation
- [ ] Connect GUI settings to `LlmFilenameScraper` [ ]
- [ ] Add visual feedback for scraper execution and errors [ ]

## Phase 5: Final Testing
- [ ] Verify Light/Dark mode transitions [ ]
- [ ] Test settings persistence after restart [ ]
- [ ] Final verification and checkpoint [ ]
