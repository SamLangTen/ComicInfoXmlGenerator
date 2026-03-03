import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path to find src/gui
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestGuiStructure(unittest.TestCase):
    @patch('customtkinter.CTk.mainloop')
    @patch('customtkinter.CTk.title')
    def test_app_initialization(self, mock_title, mock_mainloop):
        from gui.app import App
        app = App()
        self.assertIsNotNone(app)
        mock_title.assert_called_with("ComicInfoXmlGenerator")

if __name__ == "__main__":
    unittest.main()
