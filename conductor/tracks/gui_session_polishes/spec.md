# Specification: GUI Session Polishes

## Goal
To implement professional UI data management and standard selection behavior.

## Key Features

### 1. In-Memory Metadata Cache
- Maintain a dictionary `self.comic_cache = {}` where keys are file paths and values are `ComicInfo` objects.
- **Workflow:**
  - `scan()`: Clear cache (or update existing).
  - `on_file_load(path)`: If path in cache, load from cache. Otherwise, create new `ComicInfo` and add to cache.
  - `MetadataForm.on_change`: Automatically sync form field changes back to the cached object.
  - `save_current_comic()`: Use the object from the cache to perform the `inject_comic_info_xml`.

### 2. Standard Selection Logic
- Buttons in the file list will pass the `event` to their command (using `.bind("<Button-1>")`).
- **Logic:**
  - If `Command` (macOS) or `Control` (Windows/Linux) is pressed: Toggle selection of the clicked item (current behavior).
  - If NO modifier is pressed: Clear `selected_paths`, select ONLY the clicked item.
  - Always load the clicked item into the editor.

### 3. State Consistency
- Ensure the "Apply Scraper" button label and progress bar correctly interact with the cached state.
