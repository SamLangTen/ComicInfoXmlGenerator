import unittest
import os
import tempfile
import shutil
from src.scanner import scan_archives

class TestScannerIntegration(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.test_dir)
        
        # Create various dummy files
        self.files = [
            "test1.cbz", "test2.zip",
            "test3.cbr", "test4.rar",
            "test5.cb7", "test6.7z",
            "not_a_comic.txt", "image.jpg"
        ]
        for f in self.files:
            open(os.path.join(self.test_dir, f), 'w').close()

    def test_scan_archives_finds_all_supported(self):
        found = scan_archives(self.test_dir)
        found_names = [os.path.basename(f) for f in found]
        
        expected = ["test1.cbz", "test2.zip", "test3.cbr", "test4.rar", "test5.cb7", "test6.7z"]
        for exp in expected:
            self.assertIn(exp, found_names)
            
        self.assertNotIn("not_a_comic.txt", found_names)
        self.assertNotIn("image.jpg", found_names)
        self.assertEqual(len(found_names), 6)

if __name__ == "__main__":
    unittest.main()
