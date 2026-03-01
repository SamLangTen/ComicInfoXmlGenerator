# Specification: CLI Implementation

## Goal
To provide a command-line interface for `ComicInfoXmlGenerator` that can scan directories, extract metadata, and inject `ComicInfo.xml` into archives.

## Interface
The main script should be `src/cixg.py` and it should support command-line arguments.

### Supported Commands
1. **Scan**: `python src/cixg.py scan <directory>` - Lists all detected comic archive files.
2. **Generate**: `python src/cixg.py generate <directory> [--scraper {regex,oldschool,llm}] [--dry-run]` - Scans the directory, extracts metadata using the chosen scraper, and injects `ComicInfo.xml`.

### Scraper Strategies
- `regex`: Uses `RegexFilenameScraper` (default).
- `oldschool`: Uses `OldSchoolFilenameScraper`.
- `llm`: Uses `LlmFilenameScraper` (requires `LLM_API_KEY`).

### Behavior
- Recursively scans the provided directory for `.cbz` files (initially).
- For each file:
  1. Create a `ComicInfo` object with the file path.
  2. Apply the chosen scraper.
  3. Inject the resulting `ComicInfo.xml` into the archive using `src/archive.py`.
- Logs progress to stdout.
- Support `--dry-run` to show what metadata would be generated without modifying files.
