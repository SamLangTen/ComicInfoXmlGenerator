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

    def test_extended_fields_serialization_roundtrip(self):
        comic = ComicInfo(
            Series="Spider-Man",
            Number="1",
            Writer="Stan Lee",
            Penciller="Steve Ditko",
            Inker="Steve Ditko",
            Colorist="Stan Goldberg",
            Letterer="Artie Simek",
            CoverArtist="Steve Ditko",
            Editor="Stan Lee",
            Month=8,
            Day=15,
            Imprint="Marvel Imprint",
            AgeRating="Teen",
            Characters="Spider-Man, Uncle Ben",
            Teams="Avengers",
            Locations="New York",
            ScanInformation="Scanned by X",
            StoryArc="Origin",
            SeriesGroup="Marvel Universe",
            Web="https://example.com",
            BlackAndWhite="No",
            Manga="No"
        )
        
        # Serialize
        xml_str = comic.to_xml_string()
        
        # Deserialize
        new_comic = ComicInfo.from_xml_string(xml_str)
        
        # Verify
        self.assertEqual(new_comic.Series, comic.Series)
        self.assertEqual(new_comic.Writer, comic.Writer)
        self.assertEqual(new_comic.Penciller, comic.Penciller)
        self.assertEqual(new_comic.Inker, comic.Inker)
        self.assertEqual(new_comic.Colorist, comic.Colorist)
        self.assertEqual(new_comic.Letterer, comic.Letterer)
        self.assertEqual(new_comic.CoverArtist, comic.CoverArtist)
        self.assertEqual(new_comic.Editor, comic.Editor)
        self.assertEqual(new_comic.Month, comic.Month)
        self.assertEqual(new_comic.Day, comic.Day)
        self.assertEqual(new_comic.Imprint, comic.Imprint)
        self.assertEqual(new_comic.AgeRating, comic.AgeRating)
        self.assertEqual(new_comic.Characters, comic.Characters)
        self.assertEqual(new_comic.Teams, comic.Teams)
        self.assertEqual(new_comic.Locations, comic.Locations)
        self.assertEqual(new_comic.ScanInformation, comic.ScanInformation)
        self.assertEqual(new_comic.StoryArc, comic.StoryArc)
        self.assertEqual(new_comic.SeriesGroup, comic.SeriesGroup)
        self.assertEqual(new_comic.Web, comic.Web)
        self.assertEqual(new_comic.BlackAndWhite, comic.BlackAndWhite)
        self.assertEqual(new_comic.Manga, comic.Manga)

if __name__ == "__main__":
    unittest.main()
