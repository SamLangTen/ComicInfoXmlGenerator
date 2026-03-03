# Implementation Plan: GUI Session Polishes [checkpoint: bba36c3]

## Phase 1: Metadata Caching
- [x] Implement `self.comic_cache` in `App` class [bc35304]
- [x] Update `scan` and `on_file_load` to use/initialize the cache [bc35304]
- [x] Ensure `apply_scraper` updates the cache for all processed files [bc35304]

## Phase 2: Form Synchronization
- [x] Bind form field changes to update the cached `ComicInfo` object [bc35304]
- [x] Verify that switching files and returning preserves edits [bc35304]

## Phase 3: Standard Selection Logic
- [x] Update button bindings to capture modifier keys (Cmd/Ctrl) [121cd84]
- [x] Implement conditional single/multi-selection in `toggle_selection` [121cd84]

## Phase 4: Final Verification
- [x] Test caching across multiple files [121cd84]
- [x] Verify macOS/Windows selection conventions [121cd84]
- [x] Final verification and checkpoint [121cd84]

