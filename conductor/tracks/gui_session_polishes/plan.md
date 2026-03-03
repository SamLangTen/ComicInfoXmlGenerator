# Implementation Plan: GUI Session Polishes

## Phase 1: Metadata Caching
- [ ] Implement `self.comic_cache` in `App` class [ ]
- [ ] Update `scan` and `on_file_load` to use/initialize the cache [ ]
- [ ] Ensure `apply_scraper` updates the cache for all processed files [ ]

## Phase 2: Form Synchronization
- [ ] Bind form field changes to update the cached `ComicInfo` object [ ]
- [ ] Verify that switching files and returning preserves edits [ ]

## Phase 3: Standard Selection Logic
- [ ] Update button bindings to capture modifier keys (Cmd/Ctrl) [ ]
- [ ] Implement conditional single/multi-selection in `toggle_selection` [ ]

## Phase 4: Final Verification
- [ ] Test caching across multiple files [ ]
- [ ] Verify macOS/Windows selection conventions [ ]
- [ ] Final verification and checkpoint [ ]
