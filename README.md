# ComicInfoXmlGenerator

A robust tool for generating and injecting `ComicInfo.xml` metadata into comic archives (CBZ, CBR, CB7).

## Features

- **Multi-format Support**: Works with `.cbz`, `.cbr`, and `.cb7` archives.
- **Smart Scraping**:
  - **Regex**: Fast, local filename parsing.
  - **Books.com.tw**: Targeted scraping for traditional Chinese manga metadata.
  - **LLM**: Advanced metadata extraction using AI (GPT-4o-mini).
- **Parallel Task Engine**: High-performance background scraping with a persistent task pool and configurable worker threads.
- **Web UI**: Modern, responsive interface for library management, metadata editing, and real-time task monitoring.
- **CLI**: Powerful command-line interface for batch processing and automation.
- **WebSocket Integration**: Live status updates and logs streamed directly to the browser.

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js (for Web UI)

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/yourusername/ComicInfoXmlGenerator.git
    cd ComicInfoXmlGenerator
    ```

2.  Set up the Python environment:
    ```bash
    python3 -m venv venv312
    source venv312/bin/activate
    pip install -r requirements.txt
    ```

3.  Set up the Web UI:
    ```bash
    cd web
    npm install
    npm run build
    cd ..
    ```

4.  Configure the service:
    Copy `.env.example` to `.env` and add your LLM API keys if needed.

### Running the Web UI

Start the backend server:
```bash
./venv312/bin/python3 src/api/main.py
```
The UI will be available at `http://localhost:8000`.

### Using the CLI

**Scan a directory:**
```bash
./venv312/bin/python3 src/cixg.py scan /path/to/comics
```

**Generate and inject metadata:**
```bash
./venv312/bin/python3 src/cixg.py generate /path/to/comics --scraper llm
```

## Task Management

The new Parallel Scraping Task Pool allows you to trigger large batch operations without blocking the UI.
- **Configurable Workers**: Adjust `max_workers` in Settings to tune performance.
- **Automatic Retries**: Failed tasks (e.g., due to network issues) are automatically retried up to a configurable limit.
- **Persistence**: Tasks are stored in a SQLite database and will resume if the application is restarted.

## License

MIT
