# Specification: GUI Implementation

## Goal
Build a minimalist desktop interface for `ComicInfoXmlGenerator` using `CustomTkinter`.

## User Interface Design
- **Theme:** Modern (Dark/Light mode support).
- **Layout:**
  - **Top Panel:** Directory selection (Browse button) and Scraper selection (Dropdown: Regex, OldSchool, LLM).
  - **Left Sidebar:** Scrollable list of detected comic archives.
  - **Main Area:** Editable fields for the selected comic's metadata (Series, Number, Volume, Year, Publisher, Genre, Summary).
  - **Bottom Panel:** Action buttons (Scan, Dry-run All, Inject Selected, Inject All) and a progress log.

## Components
- `gui/app.py`: Main application entry point.
- `gui/views/`: Layout and widget components.
- `gui/controllers/`: Logic to glue scrapers and archive operations to the UI.

## Requirements
- `customtkinter`
- `pillow` (for potential cover image preview in the future)
