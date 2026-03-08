# Track Specification: Enable CBR and CB7 Support

## Overview
Expand the core archive handling logic to support CBR (RAR) and CB7 (7z) formats. This includes reading and writing `ComicInfo.xml` metadata, extracting cover images, and updating the search/scan logic to recognize these formats along with standard `.zip`, `.rar`, and `.7z` extensions.

## Functional Requirements
- **Format Support:**
    - **CBR:** Support both RAR4 and RAR5 formats using the `rarfile` library (requires system `unrar` for RAR5).
    - **CB7:** Support 7z archives using the `py7zr` library.
    - **Standard Formats:** Explicitly include `.zip`, `.rar`, and `.7z` in addition to `.cbz`, `.cbr`, and `.cb7`.
- **Core Operations:**
    - **Read Metadata:** Extract `ComicInfo.xml` from CBR and CB7 archives.
    - **Write Metadata:** Inject/Update `ComicInfo.xml` within CBR and CB7 archives.
    - **Cover Extraction:** Extract the first valid image file from these archives for thumbnail generation.
- **Search/Scan Logic:**
    - Update `Scanner` and `LibraryManager` to recognize the expanded list of supported extensions.
- **Dependency Management:**
    - Add `rarfile` and `py7zr` to `requirements.txt` and `tech-stack.md`.

## Non-Functional Requirements
- **Performance:** Ensure archive operations (especially injection) are safe and don't corrupt the files.
- **Error Handling:** Gracefully handle cases where the system `unrar` binary is missing or the archive is corrupted.

## Acceptance Criteria
- **Multi-format Detection:** The scanner correctly identifies `.zip`, `.rar`, `.7z`, `.cbz`, `.cbr`, and `.cb7` files.
- **Metadata Roundtrip:** `ComicInfo.xml` can be read from and written to CBR and CB7 archives without data loss.
- **Cover Thumbnails:** Covers are successfully extracted from a sample CBR and CB7 file.
- **Test Coverage:** New archive operations are verified with unit tests using sample archives.

## Out of Scope
- Support for other archive formats like `.tar`, `.gz`, or `.ace`.
- Handling password-protected archives.
- Implementing a custom RAR/7z parser from scratch (rely on `rarfile` and `py7zr`).
