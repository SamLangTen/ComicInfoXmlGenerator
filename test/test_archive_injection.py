import unittest
import os
import tempfile
import shutil
import zipfile
from src.comic_info import ComicInfo
from src.archive import inject_comic_info_xml

class TestArchiveInjection(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.test_dir)
        
        # Create a mock CBZ (ZIP)
        self.cbz_path = os.path.join(self.test_dir, "test_comic.cbz")
        with zipfile.ZipFile(self.cbz_path, 'w') as zf:
            zf.writestr("page1.jpg", b"image_data")

    def test_inject_comic_info_xml(self):
        comic = ComicInfo(Title="Archive Test")
        
        inject_comic_info_xml(self.cbz_path, comic)
        
        # Verify XML is in the archive
        with zipfile.ZipFile(self.cbz_path, 'r') as zf:
            self.assertIn("ComicInfo.xml", zf.namelist())
            xml_content = zf.read("ComicInfo.xml").decode("utf-8")
            self.assertIn("<Title>Archive Test</Title>", xml_content)

    def test_inject_missing_file_raises_error(self):
        comic = ComicInfo(Title="Archive Test")
        with self.assertRaises(FileNotFoundError):
            inject_comic_info_xml("non_existent_file.cbz", comic)

    def test_inject_invalid_format_raises_error(self):
        comic = ComicInfo(Title="Archive Test")
        invalid_path = os.path.join(self.test_dir, "test.txt")
        open(invalid_path, 'w').close()
        with self.assertRaises(ValueError):
            inject_comic_info_xml(invalid_path, comic)

if __name__ == "__main__":
    unittest.main()
