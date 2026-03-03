# Specification: Scraper Consolidation

## Goal
Refactor the scraper module to be more maintainable and intuitive.

## New Structure

### 1. `src/scraper/local_scraper.py`
- Contains `LocalFilenameScraper`.
- **Logic Flow:**
  1. Check directory context (count comic files).
  2. If context exists (>1 file), use OldSchool (Common Prefix/Suffix) logic.
  3. If no context, fallback to Regex-based pattern matching.
  4. Always perform final cleaning of extracted strings.

### 2. `src/scraper/llm_scraper.py`
- Contains `LlmFilenameScraper`.
- Responsible for all LLM-related parsing, prompt logging, and API interaction.

### 3. `src/scraper/__init__.py`
- Cleanly exports `LocalFilenameScraper` and `LlmFilenameScraper`.
- Maintains backward compatibility if needed (mapping `RegexFilenameScraper` to `LocalFilenameScraper`).

## Dependencies
- No changes to existing dependencies.
