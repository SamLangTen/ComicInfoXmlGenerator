# Specification: Advanced Scrapers

## Goal
To improve the accuracy of metadata extraction from comic archive filenames.

## Scrapers

### 1. OldSchoolFilenameScraper
- **Objective:** Extract `Series`, `Volume`, and `Number` by comparing the current file with other files in the same directory.
- **Logic:**
  1. Identify all comic archives in the same directory.
  2. Compute the Longest Common Prefix (LCP) and Longest Common Suffix (LCS) across these filenames.
  3. The common part (after cleaning) is the `Series`.
  4. The differing part contains the `Volume` or `Number`.
- **Constraint:** Must be reliable for standard numbered series (e.g., `Comic Vol 01.cbz`, `Comic Vol 02.cbz`).

### 2. LlmFilenameScraper
- **Objective:** Use an LLM to parse complex or inconsistent filenames.
- **Interface:** OpenAI-compatible API.
- **Configuration:**
  - `LLM_BASE_URL` (Environment Variable)
  - `LLM_API_KEY` (Environment Variable)
  - `LLM_MODEL` (Default: `gpt-4o-mini`)
- **Protocol:**
  - Send the filename in a specialized prompt.
  - Expect a JSON response with keys: `Series`, `Number`, `Volume`, `Year`.
- **Dependencies:** `httpx` for HTTP requests.

## Integration
- Both scrapers must implement the `Scraper` protocol defined in `src/scraper/protocol.py`.
- The `search` method will be updated to handle the new logic.
- Existing `FilenameScraper` logic (regex-based) will be kept as `RegexFilenameScraper` for fallback.
