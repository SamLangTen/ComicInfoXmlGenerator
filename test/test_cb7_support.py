import unittest
import os
import tempfile
import shutil
import py7zr
from src.comic_info import ComicInfo
from src.archive import read_comic_info_xml, inject_comic_info_xml, extract_cover_image

class TestCB7Support(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.test_dir)
        
        self.cb7_path = os.path.join(self.test_dir, "test_comic.cb7")
        img_path = os.path.join(self.test_dir, "page1.jpg")
        with open(img_path, 'wb') as f:
            f.write(b"fake_image_data_7z")
        
        # Create 7z archive
        with py7zr.SevenZipFile(self.cb7_path, 'w') as archive:
            archive.write(img_path, arcname="page1.jpg")

    def test_read_comic_info_xml_cb7(self):
        comic = read_comic_info_xml(self.cb7_path)
        self.assertIsNone(comic)

    def test_inject_and_read_metadata_cb7(self):
        comic = ComicInfo(Title="7z Test", Writer="7z Writer")
        
        # Inject
        inject_comic_info_xml(self.cb7_path, comic)
        
        # Read back
        read_comic = read_comic_info_xml(self.cb7_path)
        self.assertIsNotNone(read_comic)
        self.assertEqual(read_comic.Title, "7z Test")
        self.assertEqual(read_comic.Writer, "7z Writer")

    def test_extract_cover_image_cb7(self):
        cover_data = extract_cover_image(self.cb7_path)
        self.assertEqual(cover_data, b"fake_image_data_7z")

if __name__ == "__main__":
    unittest.main()
