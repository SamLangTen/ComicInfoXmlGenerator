import unittest
import os
import shutil
import tempfile
from pathlib import Path
from src.scanner import scan_archives

class TestArchiveScanner(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for tests
        self.test_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.test_dir)
        
        # Create some mock files
        self.files = [
            "comic1.cbz",
            "folder1/comic2.cbr",
            "folder1/folder2/comic3.cb7",
            "not_a_comic.txt",
            "folder1/image.jpg",
            ".hidden_comic.cbz"
        ]
        
        for f in self.files:
            p = Path(self.test_dir) / f
            p.parent.mkdir(parents=True, exist_ok=True)
            p.touch()

    def test_scan_archives_finds_all_formats(self):
        found_files = scan_archives(self.test_dir)
        
        # Expected relative paths
        expected = [
            "comic1.cbz",
            "folder1/comic2.cbr",
            "folder1/folder2/comic3.cb7",
            ".hidden_comic.cbz"
        ]
        
        found_relative = [os.path.relpath(f, self.test_dir) for f in found_files]
        
        self.assertEqual(len(found_relative), 4)
        for e in expected:
            self.assertIn(e, found_relative)
        
        self.assertNotIn("not_a_comic.txt", found_relative)
        self.assertNotIn("folder1/image.jpg", found_relative)

if __name__ == "__main__":
    unittest.main()
