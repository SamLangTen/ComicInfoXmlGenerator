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
            Pages=[
                ComicPageInfo.from_xml(page)
                for page in element.find("Pages") or []
            ],
        )

    def to_xml_string(self) -> str:
        return ET.tostring(self.to_xml(), encoding="utf-8").decode("utf-8")

    @classmethod
    def from_xml_string(cls, xml_data: str):
        return cls.from_xml(ET.fromstring(xml_data))
