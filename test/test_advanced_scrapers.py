import unittest
import os
import tempfile
import shutil
from src.comic_info import ComicInfo
from src.scraper.filename_scraper import OldSchoolFilenameScraper, RegexFilenameScraper, LlmFilenameScraper
from unittest.mock import patch, MagicMock

class TestOldSchoolFilenameScraper(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.scraper = OldSchoolFilenameScraper()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_directory_inference(self):
        # Create a set of files in a directory
        files = [
            "Amazing Spider-Man v01.cbz",
            "Amazing Spider-Man v02.cbz",
            "Amazing Spider-Man v03.cbz"
        ]
        for f in files:
            with open(os.path.join(self.test_dir, f), 'w') as tmp:
                tmp.write("")

        comic = ComicInfo(path=os.path.join(self.test_dir, "Amazing Spider-Man v02.cbz"))
        result = self.scraper.search(comic)
        
        self.assertEqual(result.Series, "Amazing Spider-Man")
        self.assertEqual(result.Number, "02")

    def test_complex_directory_inference(self):
        # Files with common prefix and suffix
        files = [
            "[ScanGroup] One Piece v01 [Digital].cbz",
            "[ScanGroup] One Piece v02 [Digital].cbz",
            "[ScanGroup] One Piece v03 [Digital].cbz"
        ]
        for f in files:
            with open(os.path.join(self.test_dir, f), 'w') as tmp:
                tmp.write("")

        comic = ComicInfo(path=os.path.join(self.test_dir, "[ScanGroup] One Piece v02 [Digital].cbz"))
        result = self.scraper.search(comic)
        
        # Depending on implementation, we might want "One Piece" or "[ScanGroup] One Piece v"
        # Ideally, it should be smart enough to clean up.
        self.assertEqual(result.Series, "One Piece")
        self.assertEqual(result.Number, "02")

class TestRegexFilenameScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = RegexFilenameScraper()

    def test_basic_regex(self):
        comic = ComicInfo(path="Series 001.cbz")
        result = self.scraper.search(comic)
        self.assertEqual(result.Series, "Series")
        self.assertEqual(result.Number, "001")

class TestLlmFilenameScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = LlmFilenameScraper(api_key="test_key")

    @patch('httpx.post')
    def test_llm_parsing(self, mock_post):
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": '{"Series": "Spider-Man", "Number": "01", "Volume": 1, "Year": 2024}'
                    }
                }
            ]
        }
        mock_post.return_value = mock_response

        comic = ComicInfo(path="Complex Filename [Group] (2024).cbz")
        result = self.scraper.search(comic)

        self.assertEqual(result.Series, "Spider-Man")
        self.assertEqual(result.Number, "01")
        self.assertEqual(result.Volume, 1)
        self.assertEqual(result.Year, 2024)

if __name__ == "__main__":
    unittest.main()
