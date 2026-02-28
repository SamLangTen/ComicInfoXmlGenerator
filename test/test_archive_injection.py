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

if __name__ == "__main__":
    unittest.main()
