# Specification: Logging Optimization

## Goal
Provide transparency for LLM operations by routing technical logs to the user interface and terminal.

## Functional Requirements

### 1. Protocol Update (`src/scraper/protocol.py`)
- Add `log_callback: Optional[Callable[[str], None]] = None` to `search` and `search_batch` methods.

### 2. LLM Scraper Implementation (`src/scraper/llm_scraper.py`)
- When `search_batch` is called:
  - Generate a string representing the JSON payload (system prompt + user message).
  - Pass this string to `log_callback`.
  - Upon receiving a response, pass the raw JSON string to `log_callback`.
  - Maintain existing `print()` calls for terminal users.

### 3. GUI Integration (`gui/app.py`)
- Define a lambda or method that wraps `self.log` with `self.after(0, ...)` to be used as the `log_callback`.
- Pass this callback to the scraper in the background thread.

## Non-Functional Requirements
- **Thread Safety**: Callbacks from background threads must be handled safely by the GUI main thread.
- **Readability**: Format large JSON blocks with indentation in the log window if possible.
