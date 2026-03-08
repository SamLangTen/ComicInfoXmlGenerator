import zipfile
import tempfile
import shutil
import os
import subprocess
from typing import Optional
from src.comic_info import ComicInfo

# Optional imports for other archive formats
try:
    import rarfile
    # Configure to use system unrar for RAR5 support
    rarfile.UNRAR_TOOL = "unrar"
except ImportError:
    rarfile = None

try:
    import py7zr
except ImportError:
    py7zr = None

def _get_supported_extensions():
    exts = ['.cbz', '.zip']
    if rarfile:
        exts.extend(['.cbr', '.rar'])
    if py7zr:
        exts.extend(['.cb7', '.7z'])
    return tuple(exts)

def extract_cover_image(archive_path: str) -> Optional[bytes]:
    """
    Extracts the first image from the specified archive to use as a cover.
    Returns the image bytes or None if no image is found.
    """
    if not os.path.exists(archive_path):
        return None
    
    path_lower = archive_path.lower()
    valid_image_exts = ('.jpg', '.jpeg', '.png', '.webp')
    
    # 1. ZIP/CBZ
    if path_lower.endswith(('.cbz', '.zip')):
        try:
            with zipfile.ZipFile(archive_path, 'r') as zin:
                files = sorted(zin.namelist())
                for file_name in files:
                    if file_name.lower().endswith(valid_image_exts) and not file_name.startswith('__MACOSX'):
                        return zin.read(file_name)
        except Exception as e:
            print(f"Error extracting cover from ZIP {archive_path}: {e}")

    # 2. RAR/CBR
    elif path_lower.endswith(('.cbr', '.rar')) and rarfile:
        try:
            with rarfile.RarFile(archive_path, 'r') as rin:
                files = sorted(rin.namelist())
                for file_name in files:
                    if file_name.lower().endswith(valid_image_exts):
                        return rin.read(file_name)
        except Exception as e:
            print(f"Error extracting cover from RAR {archive_path}: {e}")

    # 3. 7z/CB7
    elif path_lower.endswith(('.cb7', '.7z')) and py7zr:
        try:
            with py7zr.SevenZipFile(archive_path, mode='r') as sin:
                # sin.getnames() returns a list of filenames
                files = sorted(sin.getnames())
                for file_name in files:
                    if file_name.lower().endswith(valid_image_exts):
                        # py7zr.read returns a dict of {filename: BytesIO}
                        data_dict = sin.read([file_name])
                        return data_dict[file_name].read()
        except Exception as e:
            print(f"Error extracting cover from 7z {archive_path}: {e}")
        
    return None

def read_comic_info_xml(archive_path: str) -> Optional[ComicInfo]:
    """
    Reads the ComicInfo.xml metadata from the specified archive.
    """
    if not os.path.exists(archive_path):
        return None
    
    path_lower = archive_path.lower()
    
    # 1. ZIP/CBZ
    if path_lower.endswith(('.cbz', '.zip')):
        try:
            with zipfile.ZipFile(archive_path, 'r') as zin:
                if 'ComicInfo.xml' in zin.namelist():
                    xml_content = zin.read('ComicInfo.xml').decode('utf-8')
                    return ComicInfo.from_xml_string(xml_content, path=archive_path)
        except Exception as e:
            print(f"Error reading ComicInfo.xml from ZIP {archive_path}: {e}")

    # 2. RAR/CBR
    elif path_lower.endswith(('.cbr', '.rar')) and rarfile:
        try:
            with rarfile.RarFile(archive_path, 'r') as rin:
                if 'ComicInfo.xml' in rin.namelist():
                    xml_content = rin.read('ComicInfo.xml').decode('utf-8')
                    return ComicInfo.from_xml_string(xml_content, path=archive_path)
        except Exception as e:
            print(f"Error reading ComicInfo.xml from RAR {archive_path}: {e}")

    # 3. 7z/CB7
    elif path_lower.endswith(('.cb7', '.7z')) and py7zr:
        try:
            with py7zr.SevenZipFile(archive_path, mode='r') as sin:
                if 'ComicInfo.xml' in sin.getnames():
                    data_dict = sin.read(['ComicInfo.xml'])
                    xml_content = data_dict['ComicInfo.xml'].read().decode('utf-8')
                    return ComicInfo.from_xml_string(xml_content, path=archive_path)
        except Exception as e:
            print(f"Error reading ComicInfo.xml from 7z {archive_path}: {e}")
    
    return None

def inject_comic_info_xml(archive_path: str, comic: ComicInfo):
    """
    Injects the ComicInfo.xml metadata into the specified archive.
    """
    if not os.path.exists(archive_path):
        raise FileNotFoundError(f"Archive not found: {archive_path}")
    
    path_lower = archive_path.lower()
    xml_str = '<?xml version="1.0" encoding="utf-8"?>\n' + comic.to_xml_string()
    
    # 1. ZIP/CBZ
    if path_lower.endswith(('.cbz', '.zip')):
        # Use a temporary file for safe replacement
        temp_fd, temp_path = tempfile.mkstemp(dir=os.path.dirname(archive_path))
        os.close(temp_fd)
        try:
            with zipfile.ZipFile(archive_path, 'r') as zin:
                with zipfile.ZipFile(temp_path, 'w') as zout:
                    for item in zin.infolist():
                        if item.filename != 'ComicInfo.xml':
                            zout.writestr(item, zin.read(item.filename))
                    zout.writestr('ComicInfo.xml', xml_str)
            shutil.move(temp_path, archive_path)
        finally:
            if os.path.exists(temp_path):
                try: os.remove(temp_path)
                except OSError: pass

    # 2. RAR/CBR (Requires 'rar' binary)
    elif path_lower.endswith(('.cbr', '.rar')):
        # Writing to RAR is not supported by rarfile, we must use the 'rar' command
        temp_dir = tempfile.mkdtemp()
        xml_path = os.path.join(temp_dir, "ComicInfo.xml")
        try:
            with open(xml_path, "w", encoding="utf-8") as f:
                f.write(xml_str)
            
            # -ep: exclude paths
            result = subprocess.run(["rar", "a", "-ep", archive_path, xml_path], capture_output=True)
            if result.returncode != 0:
                raise RuntimeError(f"Failed to inject XML into RAR: {result.stderr.decode()}")
        finally:
            shutil.rmtree(temp_dir)

    # 3. 7z/CB7
    elif path_lower.endswith(('.cb7', '.7z')) and py7zr:
        # py7zr supports appending/updating by re-creating or using SevenZipFile in some modes
        # Simplest safe way: extract everything to temp and re-compress
        temp_dir = tempfile.mkdtemp()
        try:
            with py7zr.SevenZipFile(archive_path, mode='r') as sin:
                sin.extractall(path=temp_dir)
            
            # Remove old ComicInfo.xml if it exists in the extracted files
            old_xml = os.path.join(temp_dir, "ComicInfo.xml")
            if os.path.exists(old_xml):
                os.remove(old_xml)
                
            # Write new one
            with open(os.path.join(temp_dir, "ComicInfo.xml"), "w", encoding="utf-8") as f:
                f.write(xml_str)
            
            # Re-compress
            with py7zr.SevenZipFile(archive_path, mode='w') as sout:
                sout.writeall(temp_dir, arcname='')
        finally:
            shutil.rmtree(temp_dir)
    else:
        raise ValueError(f"Unsupported archive format: {archive_path}")
