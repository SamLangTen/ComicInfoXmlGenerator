# Specification: GUI UX Enhancements

## Goal
To improve the responsiveness and transparency of the CIXG GUI by offloading long-running tasks to background threads and providing visual feedback.

## Key Enhancements

### 1. Asynchronous Scraper Execution
- Offload `scraper.search` calls to a Python `threading.Thread`.
- Use `app.after()` to schedule UI updates (loading results into the form) once the thread completes.
- Ensure the "Inject Metadata" button also handles potential long-running IO similarly if needed.

### 2. Manual Scraper Trigger
- Modify the logic so selecting a file *only* loads its basic info.
- Add a dedicated "Apply Scraper" button next to the Strategy menu.
- Only execute the scraping logic when this button is clicked.

### 3. Visual Progress Feedback
- Add an indeterminate `ctk.CTkProgressBar` at the bottom of the Editor tab (or sidebar).
- Start the progress bar when a background task begins; stop it when the task ends.

### 4. LLM Request Transparency
- Modify `LlmFilenameScraper` to print the system prompt and user message to the console/stdout.
- This allows the user to inspect exactly what is being sent to the API.
