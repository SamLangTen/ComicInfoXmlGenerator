import unittest
import xml.etree.ElementTree as ET
from src.comic_info import ComicInfo, ComicPageInfo

class TestComicInfoXml(unittest.TestCase):
    def test_full_serialization_roundtrip(self):
        comic = ComicInfo(
            Title="Test Title",
            Series="Test Series",
            Number="1",
            Count=10,
            Volume=2,
            Summary="A test summary",
            Publisher="Test Publisher",
            Genre="Action",
            PageCount=1,
            LanguageISO="en",
            Year=2024
        )
        comic.Pages.append(ComicPageInfo(Image=0, Type="FrontCover"))
        
        # Serialize
        xml_str = comic.to_xml_string()
        
        # Deserialize
        new_comic = ComicInfo.from_xml_string(xml_str)
        
        # Verify
        self.assertEqual(new_comic.Title, comic.Title)
        self.assertEqual(new_comic.Series, comic.Series)
        self.assertEqual(new_comic.Number, comic.Number)
        self.assertEqual(new_comic.Count, comic.Count)
        self.assertEqual(new_comic.Volume, comic.Volume)
        self.assertEqual(new_comic.Summary, comic.Summary)
        self.assertEqual(new_comic.Publisher, comic.Publisher)
        self.assertEqual(new_comic.Genre, comic.Genre)
        self.assertEqual(new_comic.PageCount, comic.PageCount)
        self.assertEqual(new_comic.LanguageISO, comic.LanguageISO)
        self.assertEqual(new_comic.Year, comic.Year)
        self.assertEqual(len(new_comic.Pages), 1)
        self.assertEqual(new_comic.Pages[0].Image, 0)
        self.assertEqual(new_comic.Pages[0].Type, "FrontCover")

if __name__ == "__main__":
    unittest.main()
