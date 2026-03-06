# Specification: Background Service & Series Management

## Goal
Transform the application into a background service that manages a comic library by grouping archives into series and providing a continuous scanning mechanism.

## Functional Requirements
1.  **Directory Selection (First Run):**
    *   On the first run of the Web UI, the user must be prompted to select a "Manga Root Directory".
    *   This setting should be persisted.
2.  **Background Scanning:**
    *   A background task that periodically scans the Manga Root Directory for new or updated archives (CBZ/CBR/CB7).
    *   Initial full scan on startup.
3.  **Metadata Extraction & Indexing:**
    *   For each archive, attempt to read `ComicInfo.xml`.
    *   Extract `Series` name from the XML.
4.  **Series Grouping Logic:**
    *   **Primary:** Group by `Series` tag in `ComicInfo.xml`.
    *   **Secondary (Fallback 1):** If XML is missing or `Series` is empty, use the parent folder name as the Series name.
    *   **Tertiary (Fallback 2):** Use filename similarity detection if the folder structure is flat.
5.  **Web UI - Series View:**
    *   A new view in the Web UI to browse comics grouped by Series.
    *   Show series cover (usually the cover of the first volume).
    *   Show volume list within each series.
6.  **Persistence:**
    *   Maintain a local index (e.g., a JSON file or SQLite database) of scanned files and their metadata to avoid re-reading all archives on every restart.

## Technical Requirements
-   **Backend:** FastAPI background tasks or a dedicated thread for scanning.
-   **Persistence:** `src/config_manager.py` for settings. For the library index, start with a JSON-based store for simplicity, or upgrade to SQLite if performance requires it.
-   **Frontend:** New Vue components for Series browsing and first-run setup.
