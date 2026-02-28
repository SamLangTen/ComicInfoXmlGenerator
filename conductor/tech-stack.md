# Technology Stack: ComicInfoXmlGenerator

## Language
- **Python**: The core logic is built with Python for its robust string manipulation, regex support, and clean developer experience.

## Core Libraries & Frameworks
- **xml.etree.ElementTree (Standard Library)**: Used for robust XML parsing and generation of the `ComicInfo.xml` files.
- **dataclasses (Standard Library)**: Provides structured, type-safe data models for representing comic metadata.
- **re (Standard Library)**: Utilized for high-precision filename splitting and extraction of series, volume, issue, and year metadata.
- **pathlib (Standard Library)**: Used for robust and recursive file system scanning and path manipulation.
- **unittest & pytest**: Uses Python's standard `unittest` for test structure and `pytest` (with `pytest-cov`) for test execution and coverage reporting.

## Future UI Layer (Target)
- **Proposed: Dear PyGui or Custom Tkinter**: Since the project is in Python and requires a 'good UI' but aims for 'Clean & Minimalist', these libraries are strong candidates for future UI development.

## Archive Handling (Target)
- **Proposed: zipfile, tarfile, and rarfile**: Standard libraries and specialized modules for managing the target comic archive formats (CBZ, CBR, CB7).
