import unittest
import subprocess
import os
import tempfile
import shutil

class TestCLI(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.test_dir)
        
        # Create a mock archive
        self.archive_path = os.path.join(self.test_dir, "test_comic.cbz")
        with open(self.archive_path, 'w') as f:
            f.write("dummy content")

    def test_scan_command(self):
        # Run: python3 src/cixg.py scan <test_dir>
        result = subprocess.run(
            ["venv/bin/python", "src/cixg.py", "scan", self.test_dir],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Found 1 comic(s)", result.stdout)
        self.assertIn("test_comic.cbz", result.stdout)

    def test_generate_dry_run(self):
        # Run: python3 src/cixg.py generate <test_dir> --dry-run
        result = subprocess.run(
            ["venv/bin/python", "src/cixg.py", "generate", self.test_dir, "--dry-run"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Dry-run", result.stdout)
        self.assertIn("Series: test_comic", result.stdout)

    def test_generate_real_injection(self):
        # Create a real zip file (cbz)
        import zipfile
        real_cbz = os.path.join(self.test_dir, "Real Comic 001.cbz")
        with zipfile.ZipFile(real_cbz, 'w') as zf:
            zf.writestr("page1.jpg", b"data")
            
        # Run: python3 src/cixg.py generate <test_dir> --scraper regex
        result = subprocess.run(
            ["venv/bin/python", "src/cixg.py", "generate", self.test_dir, "--scraper", "regex"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("[SUCCESS] Injected ComicInfo.xml", result.stdout)
        
        # Verify XML content
        with zipfile.ZipFile(real_cbz, 'r') as zf:
            self.assertIn("ComicInfo.xml", zf.namelist())
            xml_content = zf.read("ComicInfo.xml").decode("utf-8")
            self.assertIn("<Series>Real Comic</Series>", xml_content)
            self.assertIn("<Number>001</Number>", xml_content)

    def test_generate_with_extended_flags(self):
        # Create a real zip file (cbz)
        import zipfile
        cbz_path = os.path.join(self.test_dir, "FlagTest.cbz")
        with zipfile.ZipFile(cbz_path, 'w') as zf:
            zf.writestr("p1.jpg", b"data")
            
        # Run: python3 src/cixg.py generate <test_dir> --writer "John Doe" --characters "Hero A, Hero B" --age-rating "Teen"
        result = subprocess.run(
            [
                "venv/bin/python", "src/cixg.py", "generate", self.test_dir, 
                "--writer", "John Doe", 
                "--characters", "Hero A, Hero B",
                "--age-rating", "Teen"
            ],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        
        # Verify XML content
        with zipfile.ZipFile(cbz_path, 'r') as zf:
            xml_content = zf.read("ComicInfo.xml").decode("utf-8")
            self.assertIn("<Writer>John Doe</Writer>", xml_content)
            self.assertIn("<Characters>Hero A, Hero B</Characters>", xml_content)
            self.assertIn("<AgeRating>Teen</AgeRating>", xml_content)

if __name__ == "__main__":
    unittest.main()
