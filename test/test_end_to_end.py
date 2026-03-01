import unittest
import os
import tempfile
import shutil
import zipfile
from src.scanner import scan_archives
from src.scraper import FilenameScraper
from src.comic_info import ComicInfo
from src.archive import inject_comic_info_xml

class TestEndToEnd(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.test_dir)
        
        # Create a mock archive with a specific name
        self.archive_name = "The Amazing Spider-Man #001 (2024).cbz"
        self.archive_path = os.path.join(self.test_dir, self.archive_name)
        with zipfile.ZipFile(self.archive_path, 'w') as zf:
            zf.writestr("page1.jpg", b"fake_image")

    def test_full_pipeline(self):
        # 1. Scan
        found = scan_archives(self.test_dir)
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0], self.archive_path)
        
        # 2. Scrape from filename
        comic = ComicInfo(path=found[0])
        scraper = FilenameScraper()
        scraper.search(comic)
        
        self.assertEqual(comic.Series, "The Amazing Spider-Man")
        self.assertEqual(comic.Number, "001")
        self.assertEqual(comic.Year, 2024)
        
        # 3. Inject XML
        inject_comic_info_xml(self.archive_path, comic)
        
        # 4. Verify by reading it back
        with zipfile.ZipFile(self.archive_path, 'r') as zf:
            self.assertIn("ComicInfo.xml", zf.namelist())
            xml_data = zf.read("ComicInfo.xml").decode("utf-8")
            
            re_read_comic = ComicInfo.from_xml_string(xml_data)
            self.assertEqual(re_read_comic.Series, "The Amazing Spider-Man")
            self.assertEqual(re_read_comic.Number, "001")
            self.assertEqual(re_read_comic.Year, 2024)

if __name__ == "__main__":
    unittest.main()
