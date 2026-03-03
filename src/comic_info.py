from dataclasses import dataclass, field
from typing import List, Optional
import xml.etree.ElementTree as ET

@dataclass
class ComicPageInfo:
    Image: int
    Type: str = "Story"
    DoublePage: bool = False
    ImageSize: int = 0
    Key: str = ""
    Bookmark: str = ""
    ImageWidth: int = -1
    ImageHeight: int = -1

    def to_xml(self) -> ET.Element:
        page_elem = ET.Element("Page")
        page_elem.set("Image", str(self.Image))
        page_elem.set("Type", self.Type)
        page_elem.set("DoublePage", str(self.DoublePage).lower())
        page_elem.set("ImageSize", str(self.ImageSize))
        page_elem.set("Key", self.Key)
        page_elem.set("Bookmark", self.Bookmark)
        page_elem.set("ImageWidth", str(self.ImageWidth))
        page_elem.set("ImageHeight", str(self.ImageHeight))
        return page_elem

    @classmethod
    def from_xml(cls, element: ET.Element):
        return cls(
            Image=int(element.get("Image", 0)),
            Type=element.get("Type", "Story"),
            DoublePage=element.get("DoublePage", "false") == "true",
            ImageSize=int(element.get("ImageSize", 0)),
            Key=element.get("Key", ""),
            Bookmark=element.get("Bookmark", ""),
            ImageWidth=int(element.get("ImageWidth", -1)),
            ImageHeight=int(element.get("ImageHeight", -1)),
        )

@dataclass
class ComicInfo:
    Title: str = ""
    Series: str = ""
    Number: str = ""
    Count: int = -1
    Volume: int = -1
    Summary: str = ""
    Publisher: str = ""
    Genre: str = ""
    PageCount: int = 0
    LanguageISO: str = ""
    Pages: List[ComicPageInfo] = field(default_factory=list)
    path: Optional[str] = None
    Year: int = -1
    Month: int = -1
    Day: int = -1
    Writer: str = ""
    Penciller: str = ""
    Inker: str = ""
    Colorist: str = ""
    Letterer: str = ""
    CoverArtist: str = ""
    Editor: str = ""
    Imprint: str = ""
    AgeRating: str = ""
    Characters: str = ""
    Teams: str = ""
    Locations: str = ""
    ScanInformation: str = ""
    StoryArc: str = ""
    SeriesGroup: str = ""
    Web: str = ""
    BlackAndWhite: str = "Unknown" # Yes, No, Unknown
    Manga: str = "Unknown" # Yes, No, Unknown

    def to_xml(self) -> ET.Element:
        root = ET.Element("ComicInfo")
        ET.SubElement(root, "Title").text = self.Title
        ET.SubElement(root, "Series").text = self.Series
        ET.SubElement(root, "Number").text = self.Number
        ET.SubElement(root, "Count").text = str(self.Count)
        ET.SubElement(root, "Volume").text = str(self.Volume)
        ET.SubElement(root, "Summary").text = self.Summary
        ET.SubElement(root, "Publisher").text = self.Publisher
        ET.SubElement(root, "Genre").text = self.Genre
        ET.SubElement(root, "PageCount").text = str(self.PageCount)
        ET.SubElement(root, "LanguageISO").text = self.LanguageISO
        if self.Year != -1:
            ET.SubElement(root, "Year").text = str(self.Year)
        if self.Month != -1:
            ET.SubElement(root, "Month").text = str(self.Month)
        if self.Day != -1:
            ET.SubElement(root, "Day").text = str(self.Day)
        
        ET.SubElement(root, "Writer").text = self.Writer
        ET.SubElement(root, "Penciller").text = self.Penciller
        ET.SubElement(root, "Inker").text = self.Inker
        ET.SubElement(root, "Colorist").text = self.Colorist
        ET.SubElement(root, "Letterer").text = self.Letterer
        ET.SubElement(root, "CoverArtist").text = self.CoverArtist
        ET.SubElement(root, "Editor").text = self.Editor
        ET.SubElement(root, "Imprint").text = self.Imprint
        ET.SubElement(root, "AgeRating").text = self.AgeRating
        ET.SubElement(root, "Characters").text = self.Characters
        ET.SubElement(root, "Teams").text = self.Teams
        ET.SubElement(root, "Locations").text = self.Locations
        ET.SubElement(root, "ScanInformation").text = self.ScanInformation
        ET.SubElement(root, "StoryArc").text = self.StoryArc
        ET.SubElement(root, "SeriesGroup").text = self.SeriesGroup
        ET.SubElement(root, "Web").text = self.Web
        ET.SubElement(root, "BlackAndWhite").text = self.BlackAndWhite
        ET.SubElement(root, "Manga").text = self.Manga

        pages_elem = ET.SubElement(root, "Pages")
        for page in self.Pages:
            pages_elem.append(page.to_xml())

        return root

    @classmethod
    def from_xml(cls, element: ET.Element):
        return cls(
            Title=element.findtext("Title", ""),
            Series=element.findtext("Series", ""),
            Number=element.findtext("Number", ""),
            Count=int(element.findtext("Count", -1)),
            Volume=int(element.findtext("Volume", -1)),
            Summary=element.findtext("Summary", ""),
            Publisher=element.findtext("Publisher", ""),
            Genre=element.findtext("Genre", ""),
            PageCount=int(element.findtext("PageCount", 0)),
            LanguageISO=element.findtext("LanguageISO", ""),
            Year=int(element.findtext("Year", -1)),
            Month=int(element.findtext("Month", -1)),
            Day=int(element.findtext("Day", -1)),
            Writer=element.findtext("Writer", ""),
            Penciller=element.findtext("Penciller", ""),
            Inker=element.findtext("Inker", ""),
            Colorist=element.findtext("Colorist", ""),
            Letterer=element.findtext("Letterer", ""),
            CoverArtist=element.findtext("CoverArtist", ""),
            Editor=element.findtext("Editor", ""),
            Imprint=element.findtext("Imprint", ""),
            AgeRating=element.findtext("AgeRating", ""),
            Characters=element.findtext("Characters", ""),
            Teams=element.findtext("Teams", ""),
            Locations=element.findtext("Locations", ""),
            ScanInformation=element.findtext("ScanInformation", ""),
            StoryArc=element.findtext("StoryArc", ""),
            SeriesGroup=element.findtext("SeriesGroup", ""),
            Web=element.findtext("Web", ""),
            BlackAndWhite=element.findtext("BlackAndWhite", "Unknown"),
            Manga=element.findtext("Manga", "Unknown"),
            Pages=[
                ComicPageInfo.from_xml(page)
                for page in (element.find("Pages") if element.find("Pages") is not None else [])
            ],
        )

    def to_xml_string(self) -> str:
        return ET.tostring(self.to_xml(), encoding="utf-8").decode("utf-8")

    @classmethod
    def from_xml_string(cls, xml_data: str):
        return cls.from_xml(ET.fromstring(xml_data))


def write_comic_info_xml(comic: ComicInfo, file_path: str):
    """Writes the ComicInfo object to an XML file at the specified path."""
    xml_str = comic.to_xml_string()
    with open(file_path, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write(xml_str)
