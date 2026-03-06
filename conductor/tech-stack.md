# Technology Stack: ComicInfoXmlGenerator

## Language
- **Python**: The core logic is built with Python for its robust string manipulation, regex support, and clean developer experience.

## Core Libraries & Frameworks
- **xml.etree.ElementTree (Standard Library)**: Used for robust XML parsing and generation of the `ComicInfo.xml` files.
- **dataclasses (Standard Library)**: Provides structured, type-safe data models for representing comic metadata.
- **typing.Protocol**: Used to define a flexible, structural interface for scrapers, ensuring extensibility for future online metadata sources.
- **re (Standard Library)**: Utilized for high-precision filename splitting and extraction of series, volume, issue, and year metadata.
- **pathlib (Standard Library)**: Used for robust and recursive file system scanning and path manipulation.
- **httpx**: Used for calling OpenAI-compatible APIs in `LlmFilenameScraper`.
- **python-dotenv**: Used for managing API keys and configuration via `.env` files.
- **customtkinter**: Modern, minimalist UI framework built on top of Tkinter.
- **Pillow**: Used for image handling (comic covers).
- **unittest & pytest**: Uses Python's standard `unittest` for test structure and `pytest` (with `pytest-cov`) for test execution and coverage reporting.

## UI Layer
- **Desktop**: **customtkinter** – Modern, minimalist UI framework built on top of Tkinter.
- **Web**: **Vue 3 + TypeScript** – Reactive, component-based frontend framework.
- **Web Styling**: **Tailwind CSS** – Utility-first CSS framework for modern web design.
- **Web Backend**: **FastAPI** – High-performance Python API framework for serving the Web UI and exposing core logic.
- **Networking**: **Axios** – Promise-based HTTP client for API communication.
- **Real-time Logs**: **WebSockets** – Used for streaming live technical logs to the browser.

## Core Libraries & Frameworks

- **zipfile (Standard Library)**: Used for robust metadata injection into CBZ archives.
- **Proposed: tarfile and rarfile**: Future support for CBR and CB7 archive formats.
