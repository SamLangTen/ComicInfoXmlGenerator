import unittest
from src.comic_info import ComicInfo
from src.filename_scraper import FilenameScraper
import os

class TestFilenameScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = FilenameScraper()

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
        # Assuming we add Year to ComicInfo later, or check if we store it
        # For now let's focus on Series, Volume, Number

    def test_filename_with_year_and_no_volume(self):
        comic = ComicInfo(path="Batman (2020) #05.cbr")
        result = self.scraper.search(comic)
        self.assertEqual(result.Series, "Batman")
        self.assertEqual(result.Number, "05")

if __name__ == "__main__":
    unittest.main()
