import unittest
import os
import tempfile
import shutil
from src.comic_info import ComicInfo, write_comic_info_xml

class TestXmlWriter(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.test_dir)

    def test_write_comic_info_xml(self):
        comic = ComicInfo(Title="Test Comic")
        file_path = os.path.join(self.test_dir, "ComicInfo.xml")
        
        write_comic_info_xml(comic, file_path)
        
        # Verify file exists and has content
        self.assertTrue(os.path.exists(file_path))
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("<Title>Test Comic</Title>", content)
            self.assertTrue(content.startswith('<?xml version="1.0" encoding="utf-8"?>'))

if __name__ == "__main__":
    unittest.main()
