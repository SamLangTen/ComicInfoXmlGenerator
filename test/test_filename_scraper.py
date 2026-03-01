import unittest
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from src.comic_info import ComicInfo
from src.scraper import FilenameScraper, RegexFilenameScraper, OldSchoolFilenameScraper, LlmFilenameScraper

class TestRegexFilenameScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = RegexFilenameScraper()

    def test_basic_filename(self):
        comic = ComicInfo(path="Series 001.cbz")
        result = self.scraper.search(comic)
        self.assertEqual(result.Series, "Series")
        self.assertEqual(result.Number, "001")

    def test_complex_filename(self):
        comic = ComicInfo(path="Amazing Spider-Man V01 #01 (2024).cbz")
        result = self.scraper.search(comic)
        self.assertEqual(result.Series, "Amazing Spider-Man")
        self.assertEqual(result.Volume, 1)
        self.assertEqual(result.Number, "01")
        self.assertEqual(result.Year, 2024)

    def test_filename_with_year_and_no_volume(self):
        comic = ComicInfo(path="Batman (2020) #05.cbr")
        result = self.scraper.search(comic)
        self.assertEqual(result.Series, "Batman")
        self.assertEqual(result.Number, "05")
        self.assertEqual(result.Year, 2020)

class TestOldSchoolFilenameScraper(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.scraper = OldSchoolFilenameScraper()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_directory_inference(self):
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
