# Implementation Plan: Enable CBR and CB7 Support

## Phase 1: Environment and Dependencies [checkpoint: 167c8d1]
- [x] Task: Update `requirements.txt` with `rarfile` and `py7zr`. 05accd7
- [x] Task: Update `conductor/tech-stack.md` to reflect the new libraries. bdae3b1
- [x] Task: Verify availability of `unrar` binary on the system (required for `rarfile` handling RAR5). (Installed via brew)
- [x] Task: Conductor - User Manual Verification 'Environment and Dependencies' (Protocol in workflow.md) 167c8d1

## Phase 2: Core Archive Logic (CBR/RAR)
- [x] Task: Implement `read_comic_info_xml`, `inject_comic_info_xml`, and `extract_cover_image` for CBR files in `src/archive.py` using `rarfile`. 316c9d9
    - [x] Write failing unit tests for CBR operations.
    - [x] Implement the logic.
    - [x] Verify with tests.
- [x] Task: Conductor - User Manual Verification 'Core Archive Logic (CBR/RAR)' (Protocol in workflow.md) 316c9d9

## Phase 3: Core Archive Logic (CB7/7z)
- [x] Task: Implement `read_comic_info_xml`, `inject_comic_info_xml`, and `extract_cover_image` for CB7 files in `src/archive.py` using `py7zr`. efdec9d
    - [x] Write failing unit tests for CB7 operations.
    - [x] Implement the logic.
    - [x] Verify with tests.
- [x] Task: Conductor - User Manual Verification 'Core Archive Logic (CB7/7z)' (Protocol in workflow.md) efdec9d

## Phase 4: Scanner and Search Integration [checkpoint: a2299e9]
- [x] Task: Update `src/scanner.py` and `src/library_manager.py` to include `.zip`, `.rar`, `.7z`, `.cbz`, `.cbr`, and `.cb7` in supported extensions. 316c9d9
- [x] Task: Refactor `src/archive.py` to provide a unified interface (factory or dispatcher) for all supported archive types. 316c9d9
- [x] Task: Verify that the scanner detects and processes all new formats correctly. 98d7fdc
- [x] Task: Conductor - User Manual Verification 'Scanner and Search Integration' (Protocol in workflow.md) a2299e9
