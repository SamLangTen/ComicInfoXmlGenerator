from src.scraper import FilenameScraper
from src.comic_info import ComicInfo

filenames = [
    "./第2期/21[MELTY BLOOD逝血之戰][TYPE-MOON×フランスパン×桐嶋たける][角川][1-9完] [电子版][JPG]/MELTY BLOOD逝血之戰 09.cbz"
]

comics = [ComicInfo(path=c) for c in filenames]
scraper = FilenameScraper()
for c in comics:
    scraper.search(c)
