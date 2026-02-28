import zipfile
import tempfile
import shutil
import os
from src.comic_info import ComicInfo

def inject_comic_info_xml(archive_path: str, comic: ComicInfo):
    """
    Injects the ComicInfo.xml metadata into the specified .cbz archive.
    """
    if not os.path.exists(archive_path):
        raise FileNotFoundError(f"Archive not found: {archive_path}")
    
    if not archive_path.lower().endswith('.cbz'):
        raise ValueError(f"Only .cbz archives are supported currently: {archive_path}")
    
    xml_str = '<?xml version="1.0" encoding="utf-8"?>\n' + comic.to_xml_string()
    
    # Use a temporary file for safe replacement
    temp_fd, temp_path = tempfile.mkstemp(dir=os.path.dirname(archive_path))
    os.close(temp_fd)
    
    try:
        with zipfile.ZipFile(archive_path, 'r') as zin:
            with zipfile.ZipFile(temp_path, 'w') as zout:
                # Copy all existing files except ComicInfo.xml
                for item in zin.infolist():
                    if item.filename != 'ComicInfo.xml':
                        zout.writestr(item, zin.read(item.filename))
                
                # Add the new ComicInfo.xml
                zout.writestr('ComicInfo.xml', xml_str)
        
        # Replace the original archive
        shutil.move(temp_path, archive_path)
    finally:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass
