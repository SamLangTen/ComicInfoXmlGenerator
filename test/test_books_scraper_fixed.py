import unittest
from unittest.mock import patch, MagicMock
from src.scraper.books_scraper import BooksScraper
from src.comic_info import ComicInfo

class TestBooksScraperFixed(unittest.TestCase):
    def setUp(self):
        self.scraper = BooksScraper()
        with open("search_results.html", "r", encoding="utf-8") as f:
            self.search_html = f.read()
        with open("detail_page.html", "r", encoding="utf-8") as f:
            self.detail_html = f.read()
        with open("frieren_1.html", "r", encoding="utf-8") as f:
            self.frieren_html = f.read()

    @patch("httpx.Client.get")
    def test_search_and_parse_fire_phoenix(self, mock_get):
        mock_search_resp = MagicMock()
        mock_search_resp.status_code = 200
        mock_search_resp.text = self.search_html
        
        mock_detail_resp = MagicMock()
        mock_detail_resp.status_code = 200
        mock_detail_resp.text = self.detail_html
        
        mock_get.side_effect = [mock_search_resp, mock_detail_resp]

        comic = ComicInfo(Title="火鳳凰")
        result = self.scraper.search(comic)

        self.assertEqual(result.Title, "火鳳凰")
        self.assertEqual(result.Writer, "袁家倫")
        self.assertEqual(result.Publisher, "白象文化")
        self.assertEqual(result.Year, 2020)
        self.assertEqual(result.Month, 11)
        self.assertEqual(result.Day, 1)
        self.assertIn("心理勵志", result.Genre)
        self.assertIn("勵志故事/散文", result.Genre)
        self.assertIn("她如火鳳凰一般", result.Summary)

    @patch("httpx.Client.get")
    def test_search_and_parse_frieren(self, mock_get):
        mock_search_resp = MagicMock()
        mock_search_resp.status_code = 200
        mock_search_resp.text = self.search_html
        
        mock_detail_resp = MagicMock()
        mock_detail_resp.status_code = 200
        mock_detail_resp.text = self.frieren_html
        
        mock_get.side_effect = [mock_search_resp, mock_detail_resp]

        comic = ComicInfo(Title="葬送的芙莉蓮")
        result = self.scraper.search(comic)

        self.assertEqual(result.Title, "葬送的芙莉蓮 1")
        self.assertEqual(result.Volume, 1)
        self.assertTrue("山田鐘人" in result.Writer or "山田 鐘人" in result.Writer)
        self.assertEqual(result.Publisher, "東立")

    @patch("httpx.Client.get")
    def test_search_404(self, mock_get):
        mock_search_resp = MagicMock()
        mock_search_resp.status_code = 404
        mock_get.return_value = mock_search_resp
        comic = ComicInfo(Title="不存在的書")
        result = self.scraper.search(comic)
        self.assertEqual(result.Title, "不存在的書")

    @patch("httpx.Client.get")
    def test_broken_html(self, mock_get):
        # Mock search response
        mock_search_resp = MagicMock()
        mock_search_resp.status_code = 200
        mock_search_resp.text = '<html><body><div class="table-td"><h4><a href="/test">Test</a></h4></div></body></html>'
        
        # Mock "broken" detail response (missing JSON-LD and expected HTML blocks)
        mock_detail_resp = MagicMock()
        mock_detail_resp.status_code = 200
        mock_detail_resp.text = '<html><body><h1>Only Title</h1></body></html>'
        
        mock_get.side_effect = [mock_search_resp, mock_detail_resp]

        comic = ComicInfo(Title="Test Query")
        result = self.scraper.search(comic)

        # Should still have the title from the broken page, but other fields empty
        self.assertEqual(result.Title, "Only Title")
        self.assertEqual(result.Writer, "")
        self.assertEqual(result.Publisher, "")
        self.assertEqual(result.Year, -1)

if __name__ == "__main__":
    unittest.main()
