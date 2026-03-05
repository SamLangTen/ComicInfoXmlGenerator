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

    # 1. Initialize objects
    comics = [ComicInfo(path=f) for f in files]

    # 2. Batch scrape if using LLM
    if args.scraper == "llm":
        print(f"Performing batch LLM identification for {len(comics)} files...")
        scraper.search_batch(comics)

    # 3. Process each file (local scrape if needed + manual overrides + injection)
    for comic in comics:
        if args.scraper != "llm":
            scraper.search(comic)

        # Override with CLI flags if provided
        if args.title: comic.Title = args.title
        if args.series: comic.Series = args.series
        if args.number: comic.Number = args.number
        if args.volume is not None: comic.Volume = args.volume
        if args.year is not None: comic.Year = args.year
        if args.month is not None: comic.Month = args.month
        if args.day is not None: comic.Day = args.day
        if args.writer: comic.Writer = args.writer
        if args.penciller: comic.Penciller = args.penciller
        if args.inker: comic.Inker = args.inker
        if args.colorist: comic.Colorist = args.colorist
        if args.letterer: comic.Letterer = args.letterer
        if args.cover_artist: comic.CoverArtist = args.cover_artist
        if args.editor: comic.Editor = args.editor
        if args.publisher: comic.Publisher = args.publisher
        if args.imprint: comic.Imprint = args.imprint
        if args.genre: comic.Genre = args.genre
        if args.age_rating: comic.AgeRating = args.age_rating
        if args.characters: comic.Characters = args.characters
        if args.teams: comic.Teams = args.teams
        if args.locations: comic.Locations = args.locations
        if args.story_arc: comic.StoryArc = args.story_arc
        if args.series_group: comic.SeriesGroup = args.series_group
        if args.web: comic.Web = args.web
        if args.bw: comic.BlackAndWhite = args.bw
        if args.manga: comic.Manga = args.manga

        rel_path = os.path.relpath(comic.path, args.directory)
        print(f"File: {rel_path}")
        print(f"  Series: {comic.Series}")
        print(f"  Number: {comic.Number}")
        if comic.Volume != -1:
            print(f"  Volume: {comic.Volume}")
        if comic.Year != -1:
            print(f"  Year: {comic.Year}")
            
        if not args.dry_run:
            try:
                inject_comic_info_xml(comic.path, comic)
                print(f"  [SUCCESS] Injected ComicInfo.xml")
            except Exception as e:
                print(f"  [ERROR] Failed to inject: {e}")
        print("-" * 20)

def serve_command(args):
    import uvicorn
    print(f"Starting Web UI at http://{args.host}:{args.port}")
    uvicorn.run("src.api.main:app", host=args.host, port=args.port, reload=False)

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

    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Launch the Web UI server")
    serve_parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port to listen on")
    serve_parser.set_defaults(func=serve_command)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
