import os
from pathlib import Path

def scan_archives(directory: str) -> list[str]:
    """
    Recursively scan a directory for comic archive files (.cbz, .cbr, .cb7).
    """
    path = Path(directory)
    extensions = {'.cbz', '.cbr', '.cb7'}
    
    found_files = []
    for f in path.rglob('*'):
        if f.is_file() and f.suffix.lower() in extensions:
            found_files.append(str(f))
            
    return found_files
