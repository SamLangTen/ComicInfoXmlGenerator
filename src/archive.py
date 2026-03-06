import zipfile
import tempfile
import shutil
import os
from typing import Optional
from src.comic_info import ComicInfo

def extract_cover_image(archive_path: str) -> Optional[bytes]:
    """
    Extracts the first image from the specified .cbz archive to use as a cover.
    Returns the image bytes or None if no image is found.
    """
    if not os.path.exists(archive_path):
        return None
    
    if not archive_path.lower().endswith('.cbz'):
        return None
        
    valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    
    try:
        with zipfile.ZipFile(archive_path, 'r') as zin:
            # Get all files and sort them to ensure we get the "first" page
            files = sorted(zin.namelist())
            for file_name in files:
                if file_name.lower().endswith(valid_extensions) and not file_name.startswith('__MACOSX'):
                    return zin.read(file_name)
    except Exception as e:
        print(f"Error extracting cover from {archive_path}: {e}")
        
    return None

def read_comic_info_xml(archive_path: str) -> Optional[ComicInfo]:
    """
    Reads the ComicInfo.xml metadata from the specified .cbz archive.
    """
    if not os.path.exists(archive_path):
        return None
    
    if not archive_path.lower().endswith('.cbz'):
        return None
    
    try:
        with zipfile.ZipFile(archive_path, 'r') as zin:
            if 'ComicInfo.xml' in zin.namelist():
                xml_content = zin.read('ComicInfo.xml').decode('utf-8')
                return ComicInfo.from_xml_string(xml_content, path=archive_path)
    except Exception as e:
        print(f"Error reading ComicInfo.xml from {archive_path}: {e}")
    
    return None

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
