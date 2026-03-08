import unittest
import os
import tempfile
import shutil
import rarfile
import subprocess
from src.comic_info import ComicInfo
from src.archive import read_comic_info_xml, inject_comic_info_xml, extract_cover_image

class TestCBRSupport(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.test_dir)
        
        self.cbr_path = os.path.join(self.test_dir, "test_comic.cbr")
        img_path = os.path.join(self.test_dir, "page1.jpg")
        with open(img_path, 'wb') as f:
            f.write(b"fake_image_data")
        
        # Use absolute path for rar command
        result = subprocess.run(["rar", "a", "-ep", self.cbr_path, img_path], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"RAR error: {result.stderr}")
        
        if not os.path.exists(self.cbr_path):
            # Fallback if 'rar' is not in path but maybe brew installed it elsewhere
            subprocess.run(["/opt/homebrew/bin/rar", "a", "-ep", self.cbr_path, img_path])

    def test_read_comic_info_xml_cbr(self):
        if not os.path.exists(self.cbr_path):
            self.skipTest("rar binary not working as expected")
        comic = read_comic_info_xml(self.cbr_path)
        self.assertIsNone(comic)

    def test_inject_and_read_metadata_cbr(self):
        if not os.path.exists(self.cbr_path):
            self.skipTest("rar binary not working as expected")
        comic = ComicInfo(Title="CBR Test", Writer="Test Writer")
        inject_comic_info_xml(self.cbr_path, comic)
        read_comic = read_comic_info_xml(self.cbr_path)
        self.assertIsNotNone(read_comic)
        self.assertEqual(read_comic.Title, "CBR Test")

    def test_extract_cover_image_cbr(self):
        if not os.path.exists(self.cbr_path):
            self.skipTest("rar binary not working as expected")
        cover_data = extract_cover_image(self.cbr_path)
        self.assertEqual(cover_data, b"fake_image_data")

if __name__ == "__main__":
    unittest.main()
