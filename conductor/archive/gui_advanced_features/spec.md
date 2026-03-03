# Specification: GUI Advanced Features

## Goal
To implement multi-file processing and granular scraper application modes.

## Key Features

### 1. Improved Selection Visibility
- Use a distinct background color (e.g., `#1f538d`) for selected items in the scrollable file list.
- Change the button text color or border to make the selection unambiguous.

### 2. Multi-selection for Archives
- Track multiple selected file paths in a `set`.
- Support Ctrl/Cmd+Click for individual selection and Shift+Click for range selection (optional, or simple multi-toggle).
- Implement "Select All" and "Clear Selection" buttons.

### 3. Application Modes: Overwrite vs Fill Gaps
- **Overwrite (Default):** Always update the `ComicInfo` fields with values found by the scraper.
- **Fill Gaps:** Only update fields if they are currently empty or equal to their default values (e.g., `""`, `-1`).
- Add a Radio Button group in the Editor tab to select the mode.

### 4. Batch Scraper Execution
- The "Apply Scraper" button will now process ALL selected files.
- Threading will be used to loop through the selected set and update their metadata objects in the background.
