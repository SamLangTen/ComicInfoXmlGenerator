# Specification: GUI Refinement

## Goal
To enhance the CIXG GUI with theme support, persistent configuration, and functional LLM strategy integration.

## Key Features

### 1. Configuration Management
- Create a `src/config_manager.py` to handle loading/saving user settings (API keys, themes, default scraper).
- Save settings to `config.json` in the user's home directory or project root.

### 2. Settings View
- Add a new "Settings" view/tab in the GUI.
- **LLM Settings:** Inputs for API Key, Base URL, and Model.
- **Theme Settings:** Dropdown for Light/Dark/System.
- **Strategy Settings:** Default scraper selection.

### 3. Theme Restoration
- Remove the aggressive `darkdetect` monkeypatch.
- Implement a safer check for theme support.
- Allow real-time theme switching via the UI.

### 4. Scraper Logic Update
- Update `gui/app.py` to inject current settings from `ConfigManager` into scraper instances.
- Provide better error feedback if LLM fails (e.g., missing API key).
