# Implementation Plan: GUI Advanced Features

## Phase 1: Enhanced Selection UI
- [ ] Implement visual highlighting for selected items in `file_list_container` [ ]
- [ ] Add "Select All" and "Deselect All" utility buttons [ ]

## Phase 2: Multi-selection Logic
- [ ] Refactor `on_file_select` to manage a set of selected paths [ ]
- [ ] Implement toggle logic for individual items [ ]

## Phase 3: Application Modes
- [ ] Add Overwrite and Fill Gaps radio buttons to the Editor [ ]
- [ ] Implement field-merging logic based on the selected mode [ ]

## Phase 4: Batch Asynchronous Processing
- [ ] Update `apply_scraper` to iterate over multiple files [ ]
- [ ] Ensure progress bar and logs correctly reflect batch progress [ ]

## Phase 5: Final Testing
- [ ] Verify batch LLM calls and logging [ ]
- [ ] Verify "Fill Gaps" preserves existing user edits [ ]
- [ ] Final verification and checkpoint [ ]
