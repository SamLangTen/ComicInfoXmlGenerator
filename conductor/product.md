# Initial Concept

读取我指定目录下的漫画压缩包，根据现有的文件名和目录信息提取部分作者和作品信息，并根据我配置的抓取器从网络上下载数据补充，最后生成一个包含元数据的ComicInfo.xml加入到压缩包中，以便其他漫画管理软件可以识别，我希望后期能加入一个良好的用户界面。

# Product Definition: ComicInfoXmlGenerator

## Overview
ComicInfoXmlGenerator is a tool designed to enhance comic archives (CBZ, CBR, CB7) with standardized `ComicInfo.xml` metadata. This metadata allows comic media servers like Kavita and Komga to accurately identify, sort, and display comics with rich information like authors, series, and volumes.

## Target Audience
- **Kavita/Komga Users**: Collectors who want their media servers to display a beautiful, organized library.
- **Bulk Processors**: Power users who need to tag and organize thousands of files with minimal manual effort.

## Core Features
- **Advanced Filenames & Metadata Scraping**: Extract series, volume, issue, and year information from archive filenames using sophisticated regex patterns, directory context analysis (OldSchool), and LLM-powered parsing for complex naming schemes.
- **Online Data Enrichment**: Connect to online comic databases to supplement local information with official metadata.
- **Powerful CLI for Automation**: Robust command-line interface with `scan` and `generate` commands for efficient directory processing, dry-run previews, and automated metadata injection.
- **Professional Desktop Metadata Editor**: A modern, tabbed GUI with standard OS selection logic (Cmd/Ctrl+Click) for batch processing. Supports comprehensive metadata fields (Credits, Characters, Story Arcs, etc.) with real-time validation and an in-memory session cache.
- **Multi-format Support**: Native handling of CBZ (ZIP) archives for metadata injection, with planned support for CBR (RAR) and CB7 (7z).

## Design Goals
- **Clean & Minimalist UI**: A simple, fast interface that prioritizes workflow efficiency over visual clutter.
- **Extensible Scraper Architecture**: Easily add new online sources and extraction rules for different naming conventions.
- **Robust Schema Compliance**: Ensure generated XML files strictly adhere to the `ComicInfo.xsd` standard.
