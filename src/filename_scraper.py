from comic_info import ComicInfo
import re


class FilenameScraper:

    SPLIT_COMMAS = ("\[|\]|,|/")

    def __split_filename(filename: str) -> list:
        splitted_texts = re.split(FilenameScraper.SPLIT_COMMAS, filename)
        filter_empty = [ele for ele in splitted_texts if ele.strip() != ""]
        return filter_empty

    def search(comic: ComicInfo) -> ComicInfo:
        print(FilenameScraper.__split_filename(comic.filename))
        return comic
