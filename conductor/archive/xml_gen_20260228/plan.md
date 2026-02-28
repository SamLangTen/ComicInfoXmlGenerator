# Implementation Plan: ComicInfo.xml Generation and Archive Injection

## Phase 1: XML Generation Logic
- [x] Task: Finalize `ComicInfo.to_xml_string` and ensure it includes all necessary fields (e.g. Year). (135e318)
    - [x] Write tests ensuring a fully populated `ComicInfo` object produces valid XML.
    - [x] Update `to_xml` and `from_xml` if needed to be consistent.
- [x] Task: Implement a utility to write the `ComicInfo.xml` content. (0b5b790)
    - [x] Write tests for a helper function that saves the XML to a specific file path.
    - [x] Ensure UTF-8 encoding is used.

## Phase 2: Archive Injection
- [x] Task: Implement injecting the `ComicInfo.xml` file into a `.cbz` archive. (55fbab0)
    - [x] Write tests that create a mock `.cbz`, inject the XML, and verify its presence.
    - [x] Use `zipfile` to handle adding/updating the file in the ZIP archive.
- [x] Task: Verify the injected XML can be read back from the archive. (95ce5b6)
    - [x] Write integration tests to scan an archive, extract metadata, generate XML, inject it, and then re-read it to confirm no data loss.

## Phase 3: Final Verification [checkpoint: f25d922]
- [x] Task: Conductor - User Manual Verification 'Phase 1 & 2 Completion' (Protocol in workflow.md)
