# Implementation Plan: Archive Scanning and Metadata Extraction

## Phase 1: Archive File Discovery
- [x] Task: Create a recursive directory scanner that identifies `.cbz`, `.cbr`, and `.cb7` files. (167855a)
    - [x] Write tests to verify the scanner correctly lists files from a mock directory.
    - [x] Implement the scanner using `pathlib`.
- [ ] Task: Integrate the scanner with the basic `ComicInfo` data model.
    - [ ] Write tests ensuring each discovered file creates a `ComicInfo` instance with its path.
    - [ ] Update `ComicInfo` to include a `path` attribute.

## Phase 2: Filename Metadata Extraction
- [ ] Task: Refine `FilenameScraper` to extract Series, Volume, Issue, and Year.
    - [ ] Write tests with multiple sample filenames covering common naming patterns.
    - [ ] Implement robust regex in `FilenameScraper.search`.
- [ ] Task: Map extracted metadata to `ComicInfo` fields.
    - [ ] Write tests verifying the mapping of extracted strings to `ComicInfo` attributes.
    - [ ] Ensure proper type conversion (e.g., Year as an integer).

## Phase 3: Final Verification
- [ ] Task: Conductor - User Manual Verification 'Phase 1 & 2 Completion' (Protocol in workflow.md)
