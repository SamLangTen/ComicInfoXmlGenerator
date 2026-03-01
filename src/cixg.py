import argparse
import os
import sys
from src.scanner import scan_archives
from src.scraper import RegexFilenameScraper, OldSchoolFilenameScraper, LlmFilenameScraper
from src.comic_info import ComicInfo
from src.archive import inject_comic_info_xml

def get_scraper(name: str):
    if name == "oldschool":
        return OldSchoolFilenameScraper()
    elif name == "llm":
        return LlmFilenameScraper()
    else:
        return RegexFilenameScraper()

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
    gen_parser.set_defaults(func=generate_command)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
