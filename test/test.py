from filename_scraper import FilenameScraper
from comic_info import ComicInfo

filenames = [
    "./第2期/21[MELTY BLOOD逝血之戰][TYPE-MOON×フランスパン×桐嶋たける][角川][1-9完] [电子版][JPG]/MELTY BLOOD逝血之戰 09.cbz"
]

comics = [ComicInfo(c) for c in filenames]
for c in comics:
    FilenameScraper.search(c)
