# Specification: Comprehensive Metadata Support

## Overview
This track expands the `ComicInfo.xml` support in both CLI and GUI to cover a broad range of extended fields defined in the v2.1 schema. This will allow users to provide detailed credits, characters, story arcs, and other metadata.

## Functional Requirements

### 1. Data Model Expansion (`src/comic_info.py`)
- Expand `ComicInfo` dataclass to include:
    - **Credits:** Writer, Penciller, Inker, Colorist, Letterer, CoverArtist, Editor.
    - **Publishing:** Month, Day, Imprint.
    - **Classification:** AgeRating, Characters, Teams, Locations, ScanInformation, StoryArc, SeriesGroup.
    - **Web:** Web (URL).
    - **Metadata Flags:** BlackAndWhite (Yes/No/Unknown), Manga (Yes/No/Unknown).
- Update `to_xml` and `from_xml` to handle these new fields.

### 2. GUI Enhancement (`gui/app.py`)
- Replace the single-column metadata form with a **Tabbed View** to organize fields elegantly:
    - **General:** Title, Series, Number, Volume, Summary, Year, Month, Day.
    - **Credits:** Writer, Penciller, Inker, Colorist, Letterer, CoverArtist, Editor.
    - **Tags & Details:** Genre, Characters, Teams, Locations, StoryArc, SeriesGroup.
    - **Publishing & Other:** Publisher, Imprint, AgeRating, Web, Manga, BlackAndWhite.
- Implement validation feedback (e.g., highlighting invalid formats).

### 3. CLI Expansion (`src/cixg.py`)
- Add **Verbose Flags** for all new fields (e.g., `--writer`, `--characters`, `--age-rating`).
- Flags will override any data found via scrapers or existing XML.

### 4. Validation Logic
- **Type Check:** Ensure numeric fields (Day, Month) and boolean-like enums (Manga, BlackAndWhite) are valid.
- **Enum Check:** Validate `AgeRating` against standard values (e.g., "Rating Pending", "Early Childhood", etc.).
- **Credit Formatting:** Basic comma-separated string validation for multi-value fields (Characters, Teams).

## Non-Functional Requirements
- **Performance:** Tab switching should be instantaneous.
- **Schema Compliance:** Generated XML must remain valid against `ComicInfo.xsd`.

## Acceptance Criteria
- All 20+ new fields are successfully saved to and read from `ComicInfo.xml`.
- GUI tabs correctly categorize and display fields.
- CLI successfully accepts and applies extended metadata flags.
- Validation prevents common errors like invalid Age Rating strings.

## Out of Scope
- Support for niche fields not listed above (e.g., CommunityRating).
- Direct integration with online databases for *these* specific fields (this track focuses on manual/manual-over-scraping).
