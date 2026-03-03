# Implementation Plan: GUI Advanced Features [checkpoint: 5f1d7ee]

## Phase 1: Enhanced Selection UI
- [x] Implement visual highlighting for selected items in `file_list_container` [c7465ff]
- [x] Add "Select All" and "Deselect All" utility buttons [c7465ff]

## Phase 2: Multi-selection Logic
- [x] Refactor `on_file_select` to manage a set of selected paths [c7465ff]
- [x] Implement toggle logic for individual items [c7465ff]

## Phase 3: Application Modes
- [x] Add Overwrite and Fill Gaps radio buttons to the Editor [ed640cd]
- [x] Implement field-merging logic based on the selected mode [ed640cd]

## Phase 4: Batch Asynchronous Processing
- [x] Update `apply_scraper` to iterate over multiple files [09b1f50]
- [x] Ensure progress bar and logs correctly reflect batch progress [09b1f50]

## Phase 5: Final Testing
- [x] Verify batch LLM calls and logging [09b1f50]
- [x] Verify "Fill Gaps" preserves existing user edits [09b1f50]
- [x] Final verification and checkpoint [09b1f50]

