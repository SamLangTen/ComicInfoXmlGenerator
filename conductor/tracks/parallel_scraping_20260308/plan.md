# Implementation Plan: Parallel Scraping Task Pool

## Phase 1: Task Management Engine (Backend Foundation)
- [x] Task: Define `Task` database model in `src/database.py` with states (Pending, Running, Completed, Failed). dd1b440
- [x] Task: Create a `TaskPool` manager in `src/task_manager.py` to handle queueing and worker lifecycle. 63d86b2
- [x] Task: Implement the background worker logic to execute scraping tasks using existing scrapers. c145e87
- [x] Task: Implement persistent task storage and recovery on application startup. fa4321a
- [x] Task: Implement configurable retry logic with a maximum retry count. eb74674
- [ ] Task: Conductor - User Manual Verification 'Task Management Engine' (Protocol in workflow.md)

## Phase 2: API & Real-time Integration (Backend Communication)
- [ ] Task: Implement FastAPI endpoints in `src/api/main.py` for task retrieval and management.
- [ ] Task: Update existing scraping endpoints to submit jobs to the `TaskPool` asynchronously.
- [ ] Task: Integrate WebSocket broadcasting for task status and progress updates.
- [ ] Task: Add configuration settings for `max_workers` and `retry_count` in `src/config.py`.
- [ ] Task: Conductor - User Manual Verification 'API & Real-time Integration' (Protocol in workflow.md)

## Phase 3: Web UI - Tasks View & Management (Frontend Core)
- [ ] Task: Create `TasksView.vue` to display the list of active, pending, and finished tasks.
- [ ] Task: Add a new "Tasks" tab to the main navigation in `App.vue`.
- [ ] Task: Implement task actions (Retry Failed, Clear Completed) in the UI.
- [ ] Task: Create a reusable `ProgressBar` component for task monitoring.
- [ ] Task: Conductor - User Manual Verification 'Web UI - Tasks View & Management' (Protocol in workflow.md)

## Phase 4: Web UI - Inline Progress & Polish (Frontend Integration)
- [ ] Task: Add inline progress indicators to `ArchiveList.vue` and `SeriesView.vue`.
- [ ] Task: Connect the frontend to the new Task WebSockets for live status updates.
- [ ] Task: Add a visual indicator (e.g., a small badge with the active task count) to the Tasks tab.
- [ ] Task: Final polish of UI/UX for task management.
- [ ] Task: Conductor - User Manual Verification 'Web UI - Inline Progress & Polish' (Protocol in workflow.md)

## Phase 5: Final Testing & Documentation
- [ ] Task: Perform end-to-end integration testing for parallel scraping under load.
- [ ] Task: Update documentation to reflect the new task-based scraping mechanism.
- [ ] Task: Conductor - User Manual Verification 'Final Testing & Documentation' (Protocol in workflow.md)
