# test_game.py

# This file contains unit tests for the game script.
# It tests the utility functions for text wrapping, countdown screen, and end screen rendering.
# pylint: disable=no-member,undefined-variable

import unittest
from unittest.mock import patch, MagicMock
import pygame
from game import wrap_text, end_screen, countdown_screen


class TestGameUtilities(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.font = pygame.font.SysFont(None, 24)

    def test_wrap_text_simple(self):
        text = "This is a simple test for wrap text function."
        max_width = 1000  # Very wide, should return one line
        result = wrap_text(text, self.font, max_width)
        self.assertEqual(len(result), 1)

    def test_wrap_text_wrapping(self):
        text = "This is a longer sentence that should wrap into multiple lines."
        max_width = 100  # Force wrapping
        result = wrap_text(text, self.font, max_width)
        self.assertGreater(len(result), 1)

    @patch("pygame.display.flip")
    @patch("pygame.time.delay")
    def test_countdown_screen_delays_and_flips(self, mock_delay, mock_flip):
        countdown_screen()
        self.assertEqual(mock_delay.call_count, 3)
        self.assertEqual(mock_flip.call_count, 3)

    @patch("pygame.display.flip")
    def test_end_screen_renders_text(self, mock_flip):
        mock_surface = MagicMock()
        with patch("view.screen", mock_surface):
            end_screen("Logan")
            self.assertTrue(mock_surface.blit.called)
            self.assertTrue(mock_flip.called)


if __name__ == "__main__":
    unittest.main()
