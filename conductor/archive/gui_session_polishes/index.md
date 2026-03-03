# Track: GUI Session Polishes

## Overview
Polish the GUI interaction and data management:
1. **Metadata Caching**: Store `ComicInfo` objects in memory for the duration of the session. Switching between files should recall their last scraped/edited state.
2. **Standard Selection Logic**:
   - **Click**: Single selection (clears others).
   - **Cmd/Ctrl + Click**: Toggle multi-selection.

## Documents
- [Specification](./spec.md)
- [Implementation Plan](./plan.md)

## Status
- **Current Phase:** Planning
- **Progress:** 0%
