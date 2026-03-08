import os
from pathlib import Path
from src.archive import get_supported_extensions

def scan_archives(directory: str) -> list[str]:
    """
    Recursively scan a directory for supported comic archive files.
    """
    path = Path(directory)
    extensions = set(get_supported_extensions())
    
    found_files = []
    for f in path.rglob('*'):
        if f.is_file() and f.suffix.lower() in extensions:
            found_files.append(str(f))
            
    return found_files
