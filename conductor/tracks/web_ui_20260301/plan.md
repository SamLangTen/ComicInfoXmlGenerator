# Implementation Plan: Web UI Implementation

## Phase 1: Backend API Development (FastAPI)
- [ ] Task: Set up FastAPI environment, dependencies (`fastapi`, `uvicorn`), and basic app structure
- [ ] Task: Implement Configuration APIs (`GET/POST /api/config`) linked to `ConfigManager`
- [ ] Task: Implement Scanning API (`POST /api/scan`) to return detected archives
- [ ] Task: Implement Metadata APIs (`GET/POST /api/metadata`) with in-memory session cache
- [ ] Task: Implement Scraper API (`POST /api/scrape`) with support for batching
- [ ] Task: Implement Injection API (`POST /api/inject`) to trigger archive writing
- [ ] Task: Add WebSocket/SSE support for real-time scraper logs and progress
- [ ] Task: Conductor - User Manual Verification 'Backend API Development' (Protocol in workflow.md)

## Phase 2: Frontend Setup & Layout (Vue 3 + TS)
- [ ] Task: Scaffold Vue 3 project with Vite, TypeScript, and Tailwind CSS
- [ ] Task: Define the core layout (Responsive Sidebar, Main Content Area, Log Console)
- [ ] Task: Implement API client services (using `axios` or `fetch`)
- [ ] Task: Conductor - User Manual Verification 'Frontend Setup & Layout' (Protocol in workflow.md)

## Phase 3: Web-based Metadata Editor
- [ ] Task: Implement the file browser/list in the sidebar with multi-selection support
- [ ] Task: Build the Tabbed Metadata Editor (General, Credits, Tags, Publishing)
- [ ] Task: Connect form fields to the Metadata APIs with auto-save to session cache
- [ ] Task: Implement real-time validation visual cues in the web form
- [ ] Task: Conductor - User Manual Verification 'Web-based Metadata Editor' (Protocol in workflow.md)

## Phase 4: Batch Processing & Live Logs
- [ ] Task: Implement the batch scraper trigger and global progress bar
- [ ] Task: Integrate WebSockets to display technical logs (LLM requests/responses) in the Log Console
- [ ] Task: Implement batch injection with individual success/error feedback
- [ ] Task: Conductor - User Manual Verification 'Batch Processing & Live Logs' (Protocol in workflow.md)

## Phase 5: Deployment & Integration
- [ ] Task: Refactor FastAPI to serve the compiled Vue static assets
- [ ] Task: Add a new command to `src/cixg.py` to launch the web server (e.g., `python src/cixg.py serve`)
- [ ] Task: Final visual polish and responsive testing (Tablet/Mobile)
- [ ] Task: Conductor - User Manual Verification 'Deployment & Integration' (Protocol in workflow.md)
