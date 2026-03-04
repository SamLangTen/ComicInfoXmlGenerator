# Specification: Web UI Implementation

## Overview
Develop a professional web-based interface for `ComicInfoXmlGenerator` (CIXG) to support remote usage (e.g., on a NAS or server). This replaces the local desktop GUI with a modern, responsive web application.

## Functional Requirements

### 1. Backend Service (Python/FastAPI)
- **API Architecture**: Build a FastAPI server to expose the existing core logic.
- **Scanning API**: Endpoint to trigger `scan_archives` and return file lists.
- **Metadata API**: Endpoints to GET/POST `ComicInfo` data, integrating with an in-memory session cache.
- **Scraper API**: Endpoint to trigger `search_batch` (Local/LLM).
- **Injection API**: Endpoint to finalize and write XML to archives.
- **Live Feedback**: Use **WebSockets** or **SSE** to stream scraper logs and progress updates to the frontend.
- **Configuration**: API to manage `config.json` settings.

### 2. Frontend Application (Vue 3 + TypeScript)
- **Modern UI**: A responsive dashboard using **Tailwind CSS**.
- **File Browser**: A sidebar or list view to navigate detected comic archives.
- **Advanced Editor**: A tabbed form (General, Credits, etc.) to edit metadata.
- **Batch Controls**: Buttons to run scrapers on multiple selected files with a real-time progress bar.
- **Tech Console**: A dedicated section to view raw LLM requests and responses.

### 3. Remote/NAS Hosting Support
- **Static Asset Serving**: FastAPI will serve the compiled Vue application.
- **Port Configuration**: Allow setting the host and port via CLI or environment variables.

## Non-Functional Requirements
- **Responsiveness**: The UI must work well on desktop and tablet browsers.
- **Performance**: Efficient handling of large file lists.
- **Type Safety**: Full TypeScript implementation for the frontend.

## Acceptance Criteria
- User can scan a directory on the server via the web browser.
- Multi-selection and batch scraping work exactly as in the desktop UI.
- Scraper logs (LLM payloads) are visible in the web interface.
- Changes made in the Web UI are successfully injected into the server's archives.

## Out of Scope
- Multi-user account management (initially single-user/password protected).
- Advanced file management (moving/deleting files) outside of metadata injection.
