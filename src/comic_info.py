from enum import Enum

ComicInfoYesNo = Enum("ComicInfoYesNo", ("Unknown", "No", "Yes"))

ComicInfoManga = Enum("ComicInfoManga", ("Unknown",
                      "No", "Yes", "YesAndRightToLeft"))

ComicInfoAgeRating = Enum("ComicInfoAgeRating",
                          ("Unknown", "AdultsOnly18Plus", "EarlyChildhood", "Everyone", "Everyone10Plus", "G", "KidsToAdults", "M", "MA15Plus", "Mature17Plus", "PG", "R18Plus", "RatingPending", "Teen", "X18Plus"))

ComicPageType = Enum("ComicPageType", ("FrontCover", "InnerCover", "Roundup", "Story",
                     "Advertisement", "Editorial", "Letters", "Preview", "BackCover", "Other", "Deleted"))


class ComicInfo:

    def __init__(self, filename, **kwargs):
        self.filename = filename
        self.title = kwargs.get("title", "")
        self.series = kwargs.get("series", "")
        self.number = kwargs.get("number", "")
        self.count = kwargs.get("count", -1)
        self.volume = kwargs.get("volume", -1)
        self.alternate_series = kwargs.get("alternate_series", "")
        self.alternate_number = kwargs.get("alternate_number", "")
        self.alternate_count = kwargs.get("alternate_count", -1)
        self.summary = kwargs.get("summary", "")
        self.notes = kwargs.get("notes", "")
        self.year = kwargs.get("year", -1)
        self.month = kwargs.get("month", -1)
        self.day = kwargs.get("day", -1)
        self.writer = kwargs.get("writer", "")
        self.penciller = kwargs.get("penciller", "")
        self.inker = kwargs.get("inker", "")
        self.colorist = kwargs.get("colorist", "")
        self.letterer = kwargs.get("letterer", "")
        self.cover_artist = kwargs.get("cover_artist", "")
        self.editor = kwargs.get("editor", "")
        self.publisher = kwargs.get("publisher", "")
        self.imprint = kwargs.get("imprint", "")
        self.genre = kwargs.get("genre", "")
        self.web = kwargs.get("web", "")
        self.page_count = kwargs.get("page_count", 0)
        self.language_iso = kwargs.get("language_iso", "")
        self.format = kwargs.get("format", "")
        self.black_and_white = kwargs.get(
            "black_and_white", ComicInfoYesNo.Unknown)
        self.manga = kwargs.get("manga", ComicInfoManga.Unknown)
        self.characters = kwargs.get("characters", "")
        self.teams = kwargs.get("teams", "")
        self.locations = kwargs.get("locations", "")
        self.scan_information = kwargs.get("scan_information", "")
        self.story_arc = kwargs.get("story_arc", "")
        self.series_group = kwargs.get("series_group", "")
        self.age_rating = kwargs.get("age_rating", ComicInfoAgeRating.Unknown)
        self.pages = kwargs.get("pages", list())
        self.community_rating = kwargs.get("community_rating", 0)


class ComicPageInfo:
    def __init__(self, image, **kwargs):
        self.image = image
        self.story = kwargs.get("story", ComicPageType.Story)
        self.double_page = kwargs.get("double_page", False)
        self.image_size = kwargs.get("image_size", 0)
        self.key = kwargs.get("key", "")
        self.bookmark = kwargs.get("bookmark", "")
        self.image_width = kwargs.get("image_width", -1)
        self.image_height = kwargs.get("image_height", -1)
