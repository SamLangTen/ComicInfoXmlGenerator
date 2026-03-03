# Track: Advanced Scrapers

## Overview
Refactor the existing `FilenameScraper` into two distinct strategies:
1. **OldSchoolFilenameScraper**: Uses directory context and string comparison to infer series and volume/number.
2. **LlmFilenameScraper**: Uses OpenAI-compatible LLM APIs to parse complex filenames.

## Documents
- [Specification](./spec.md)
- [Implementation Plan](./plan.md)

## Status
- **Current Phase:** Planning
- **Progress:** 0%
