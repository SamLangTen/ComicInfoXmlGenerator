import unittest
from pathlib import Path
from src.scanner import scan_archives
from src.comic_info import ComicInfo
import tempfile
import shutil

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.test_dir)
        
        # Create a mock comic file
        self.comic_path = Path(self.test_dir) / "test_comic.cbz"
        self.comic_path.touch()

    def test_scanner_output_to_comic_info(self):
        found_files = scan_archives(self.test_dir)
        self.assertEqual(len(found_files), 1)
        
        # This should fail if 'path' attribute is missing from ComicInfo
        comic = ComicInfo(path=found_files[0])
        self.assertEqual(comic.path, str(self.comic_path))

if __name__ == "__main__":
    unittest.main()
