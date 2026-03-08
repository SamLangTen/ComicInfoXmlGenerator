# Specification: Parallel Scraping Task Pool

## Overview
This track introduces a robust task management system to the ComicInfoXmlGenerator Web UI, enabling parallel metadata scraping for individual comic archives. By moving away from synchronous, sequential scraping, the system will provide a more responsive and efficient user experience, allowing for multiple background operations while the user continues to interact with the library.

## User Stories
- **As a user**, I want to trigger metadata scraping for multiple comics simultaneously so that the process completes faster.
- **As a user**, I want to see a dedicated "Tasks" view to track the status of all current and past scraping operations.
- **As a user**, I want to see real-time progress indicators on individual comic files while they are being scraped.
- **As a user**, I want the task queue to persist across application restarts so that I don't lose progress on long-running batches.
- **As an administrator**, I want to configure the maximum number of concurrent workers to balance performance and resource usage (especially for LLM/API scrapers).

## Functional Requirements
- **Task Management Engine**:
    - Implement a persistent task queue (SQLite-backed) to manage scraping jobs.
    - Support for "Pending", "Running", "Completed", and "Failed" statuses.
    - Configurable worker pool size (default: 4).
    - Configurable retry mechanism (e.g., 3 retries) with exponential backoff or simple intervals.
- **Web UI Enhancements**:
    - **Dedicated Tasks Tab**: A view to list all tasks, their status, progress, and error messages.
    - **Inline Progress Bars**: Real-time progress updates in the archive list/grid view using WebSockets.
    - **Control Actions**: Buttons to "Retry All Failed", "Clear Completed", and "Pause/Resume Queue".
- **Backend API Integration**:
    - New endpoints for task management (GET `/api/tasks`, POST `/api/tasks/retry/{id}`, etc.).
    - Update existing scraping triggers to submit tasks to the pool instead of executing synchronously.
    - WebSocket events for task state transitions (`task_created`, `task_updated`, `task_completed`, `task_failed`).

## Non-Functional Requirements
- **Concurrency Safety**: Ensure that multiple workers don't attempt to modify the same archive file simultaneously.
- **Persistence**: Task state and progress must be saved to the database.
- **Observability**: Detailed logging for task transitions and errors.

## Acceptance Criteria
- [ ] Users can configure the number of parallel workers in the settings.
- [ ] Multiple scraping tasks can run in parallel without blocking the UI.
- [ ] Progress is reflected in real-time in both the "Tasks" tab and the archive list.
- [ ] Failed tasks are automatically retried according to the configuration.
- [ ] The task queue resumes correctly after a server restart.
- [ ] A new `tasks` table exists in the database to track job state.

## Out of Scope
- Manual task prioritization (re-ordering).
- Support for non-scraping tasks (e.g., file moves/renames) in this specific pool.
- Distributed task workers (multi-node setup).
