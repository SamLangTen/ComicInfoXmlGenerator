import argparse
import os
import sys
from src.scanner import scan_archives
from src.scraper import LocalFilenameScraper, LlmFilenameScraper
from src.comic_info import ComicInfo
from src.archive import inject_comic_info_xml

def get_scraper(name: str):
    if name == "llm":
        return LlmFilenameScraper()
    else:
        # Both 'regex' and 'oldschool' now consolidated into LocalFilenameScraper
        return LocalFilenameScraper()

def scan_command(args):
    files = scan_archives(args.directory)
    print(f"Found {len(files)} comic(s) in {args.directory}:")
    for f in files:
        print(f"  - {os.path.relpath(f, args.directory)}")

def generate_command(args):
    files = scan_archives(args.directory)
    scraper = get_scraper(args.scraper)
    
    if args.dry_run:
        print(f"--- Dry-run mode: Scanning {len(files)} file(s) ---")
    else:
        print(f"--- Processing {len(files)} file(s) ---")
        
    for f in files:
        comic = ComicInfo(path=f)
        scraper.search(comic)
        
        rel_path = os.path.relpath(f, args.directory)
        print(f"File: {rel_path}")
        print(f"  Series: {comic.Series}")
        print(f"  Number: {comic.Number}")
        if comic.Volume != -1:
            print(f"  Volume: {comic.Volume}")
        if comic.Year != -1:
            print(f"  Year: {comic.Year}")
            
        if not args.dry_run:
            try:
                inject_comic_info_xml(f, comic)
                print(f"  [SUCCESS] Injected ComicInfo.xml")
            except Exception as e:
                print(f"  [ERROR] Failed to inject: {e}")
        print("-" * 20)

def main():
    parser = argparse.ArgumentParser(description="ComicInfo.xml Generator (CIXG)")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    subparsers.required = True

    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Scan directory for comics")
    scan_parser.add_argument("directory", help="Directory to scan")
    scan_parser.set_defaults(func=scan_command)

    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate and inject ComicInfo.xml")
    gen_parser.add_argument("directory", help="Directory to process")
    gen_parser.add_argument("--scraper", choices=["regex", "oldschool", "llm"], default="regex", help="Scraping strategy")
    gen_parser.add_argument("--dry-run", action="store_true", help="Preview metadata without modifying files")
    
    # Extended Metadata Flags
    gen_parser.add_argument("--title", help="Comic title")
    gen_parser.add_argument("--series", help="Comic series")
    gen_parser.add_argument("--number", help="Issue number")
    gen_parser.add_argument("--volume", type=int, help="Volume number")
    gen_parser.add_argument("--year", type=int, help="Publication year")
    gen_parser.add_argument("--month", type=int, help="Publication month")
    gen_parser.add_argument("--day", type=int, help="Publication day")
    gen_parser.add_argument("--writer", help="Writer(s)")
    gen_parser.add_argument("--penciller", help="Penciller(s)")
    gen_parser.add_argument("--inker", help="Inker(s)")
    gen_parser.add_argument("--colorist", help="Colorist(s)")
    gen_parser.add_argument("--letterer", help="Letterer(s)")
    gen_parser.add_argument("--cover-artist", help="Cover artist(s)")
    gen_parser.add_argument("--editor", help="Editor(s)")
    gen_parser.add_argument("--publisher", help="Publisher")
    gen_parser.add_argument("--imprint", help="Imprint")
    gen_parser.add_argument("--genre", help="Genre")
    gen_parser.add_argument("--age-rating", help="Age rating")
    gen_parser.add_argument("--characters", help="Characters (comma separated)")
    gen_parser.add_argument("--teams", help="Teams (comma separated)")
    gen_parser.add_argument("--locations", help="Locations (comma separated)")
    gen_parser.add_argument("--story-arc", help="Story arc")
    gen_parser.add_argument("--series-group", help="Series group")
    gen_parser.add_argument("--web", help="Web URL")
    gen_parser.add_argument("--bw", choices=["Yes", "No", "Unknown"], help="Black and White")
    gen_parser.add_argument("--manga", choices=["Yes", "No", "Unknown"], help="Manga")

    gen_parser.set_defaults(func=generate_command)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
