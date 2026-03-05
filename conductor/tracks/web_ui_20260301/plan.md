# Implementation Plan: Web UI Implementation

## Phase 1: Backend API Development (FastAPI) [checkpoint: a03aa7a]
- [x] Task: Set up FastAPI environment, dependencies (`fastapi`, `uvicorn`), and basic app structure [86f0c0b]
- [x] Task: Implement Configuration APIs (`GET/POST /api/config`) linked to `ConfigManager` [6e20df5]
- [x] Task: Implement Scanning API (`POST /api/scan`) to return detected archives [09f0f9d]
- [x] Task: Implement Metadata APIs (`GET/POST /api/metadata`) with in-memory session cache [0bb2f76]
- [x] Task: Implement Scraper API (`POST /api/scrape`) with support for batching [72bfb4b]
- [x] Task: Implement Injection API (`POST /api/inject`) to trigger archive writing [a8598b6]
- [x] Task: Add WebSocket/SSE support for real-time scraper logs and progress [d087851]
- [x] Task: Conductor - User Manual Verification 'Backend API Development' (Protocol in workflow.md) [a03aa7a]

## Phase 2: Frontend Setup & Layout (Vue 3 + TS) [checkpoint: 21d0892]
- [x] Task: Scaffold Vue 3 project with Vite, TypeScript, and Tailwind CSS [870a13d]
- [x] Task: Define the core layout (Responsive Sidebar, Main Content Area, Log Console) [d64a231]
- [x] Task: Implement API client services (using `axios` or `fetch`) [7d73f20]
- [x] Task: Conductor - User Manual Verification 'Frontend Setup & Layout' (Protocol in workflow.md) [21d0892]

## Phase 3: Web-based Metadata Editor [checkpoint: dd3f55b]
- [x] Task: Implement the file browser/list in the sidebar with multi-selection support [16c3e3d]
- [x] Task: Build the Tabbed Metadata Editor (General, Credits, Tags, Publishing) [a97453a]
- [x] Task: Connect form fields to the Metadata APIs with auto-save to session cache [a97453a]
- [x] Task: Implement real-time validation visual cues in the web form [49a9d6e]
- [x] Task: Conductor - User Manual Verification 'Web-based Metadata Editor' (Protocol in workflow.md) [dd3f55b]

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
