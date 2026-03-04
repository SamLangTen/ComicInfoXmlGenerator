# Implementation Plan: Comprehensive Metadata Support

## Phase 1: Metadata Core Expansion [checkpoint: 2d2dc02]
- [x] Task: Write failing unit tests for extended `ComicInfo` fields in `test/test_comic_info_xml.py` [998d22e]
- [x] Task: Update `ComicInfo` dataclass in `src/comic_info.py` with 20+ new fields [a08b6f7]
- [x] Task: Update `to_xml` and `from_xml` logic to handle serialization [a31d74b]
- [x] Task: Verify unit tests pass (Green phase) [a31d74b]
- [x] Task: Conductor - User Manual Verification 'Metadata Core Expansion' (Protocol in workflow.md) [2d2dc02]

## Phase 2: CLI Expansion [checkpoint: dec00ce]
- [x] Task: Write failing integration tests for new CLI flags in `test/test_cli.py` [cf1fc18]
- [x] Task: Update `src/cixg.py` to include `argparse` flags for all extended fields [aa95ea3]
- [x] Task: Map CLI flags to the `ComicInfo` data model during processing [4e1d42a]
- [x] Task: Verify CLI tests pass [4e1d42a]
- [x] Task: Conductor - User Manual Verification 'CLI Expansion' (Protocol in workflow.md) [dec00ce]

## Phase 3: GUI Tabbed Restructuring
- [x] Task: Refactor `gui/app.py` to replace the simple `MetadataForm` with a `ctk.CTkTabview` [6618153]
- [x] Task: Implement 'General', 'Credits', 'Tags & Details', and 'Publishing' tabs [6618153]
- [~] Task: Wire tab inputs to the `selected_comic` object and session cache
- [ ] Task: Implement basic validation visual cues (e.g., red border for invalid types)
- [ ] Task: Conductor - User Manual Verification 'GUI Tabbed Restructuring' (Protocol in workflow.md)

## Phase 4: Validation & Final Integration
- [ ] Task: Implement specific validation logic for Age Rating and Credit string formats
- [ ] Task: Perform full end-to-end testing (Scan -> Batch Scrape -> Manual Edit -> Inject)
- [ ] Task: Final code cleanup and documentation update
- [ ] Task: Conductor - User Manual Verification 'Validation & Final Integration' (Protocol in workflow.md)
