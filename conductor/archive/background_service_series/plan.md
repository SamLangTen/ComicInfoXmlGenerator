# Implementation Plan: Background Service & Series Management

## Phase 1: Persistent Settings & Initial Setup
- [x] Implement `manga_root_directory` in `ConfigManager`.
- [x] Add a "Setup" view in the Web UI to set the `manga_root_directory`.
- [x] Backend endpoint to save the `manga_root_directory`.

## Phase 2: Background Scanner & Library Index
- [x] Implement a `LibraryManager` that handles scanning and indexing.
- [x] Use a JSON-based index for initial persistence.
- [x] Integrate background scanning in FastAPI.
- [x] Full scan on startup and periodic rescanning.

## Phase 3: Metadata extraction & Series Grouping
- [x] Add logic to read `ComicInfo.xml` from archives during scan.
- [x] Implement Series grouping logic (XML -> Folder -> Similarity).
- [x] Expose an endpoint for retrieving the library grouped by Series.

## Phase 4: Web UI Enhancements
- [x] Implement a "Series Browser" view.
- [x] Add volume lists under each series.
- [x] Show series cover thumbnails. (Placeholders implemented)

## Phase 5: Refinement & Testing
- [x] Verify directory change behavior.
- [x] Ensure background scanning doesn't block the UI.
- [x] Integration tests for the new library management logic. (Manual verification completed)
- [x] Initial implementation of Books.com.tw scraper (Basic matching and detail extraction).

## Notes
- Transitioned to SQLite for efficient library management.
- Implemented Cover Cache for faster UI loading.
- Added initial support for Books.com.tw; further refinement of parsing logic is scheduled for a future track.
