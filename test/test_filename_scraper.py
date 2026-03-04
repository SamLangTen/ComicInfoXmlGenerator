import unittest
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from src.comic_info import ComicInfo
from src.scraper import LocalFilenameScraper, LlmFilenameScraper

class TestLocalFilenameScraper(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.scraper = LocalFilenameScraper()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_regex_fallback(self):
        # Single file should use regex logic
        filename = "Amazing Spider-Man v01 (2024).cbz"
        path = os.path.join(self.test_dir, filename)
        with open(path, 'w') as f: f.write("")
        
        comic = ComicInfo(path=path)
        result = self.scraper.search(comic)
        self.assertEqual(result.Series, "Amazing Spider-Man")
        self.assertEqual(result.Volume, 1)
        self.assertEqual(result.Year, 2024)

    def test_directory_inference(self):
        # Multiple files should use context logic
        files = ["One Piece 01.cbz", "One Piece 02.cbz"]
        for f in files:
            with open(os.path.join(self.test_dir, f), 'w') as tmp: tmp.write("")
        
        comic = ComicInfo(path=os.path.join(self.test_dir, "One Piece 02.cbz"))
        result = self.scraper.search(comic)
        self.assertEqual(result.Series, "One Piece")
        self.assertEqual(result.Number, "02")

class TestLlmFilenameScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = LlmFilenameScraper(api_key="test_key")

    @patch('httpx.post')
    def test_llm_parsing(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": '{"comics": [{"Filename": "Complex Filename [Group] (2024).cbz", "Series": "Spider-Man", "Number": "01", "Volume": 1, "Year": 2024}]}'
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
