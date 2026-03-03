# Track: Scraper Consolidation

## Overview
Simplify the scraper module structure:
1. **Local Consolidation**: Combine `RegexFilenameScraper` and `OldSchoolFilenameScraper` into `src/scraper/local_scraper.py` as `LocalFilenameScraper`.
2. **LLM Separation**: Move `LlmFilenameScraper` to `src/scraper/llm_scraper.py`.
3. **API Cleanup**: Update exports and internal imports to reflect the new file structure.

## Documents
- [Specification](./spec.md)
- [Implementation Plan](./plan.md)

## Status
- **Current Phase:** Planning
- **Progress:** 0%
