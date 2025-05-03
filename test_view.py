"""
test_view.py

This module contains unit tests for the rendering functions defined in view.py.
"""

import unittest
import pygame
from model import Model
import view
from settings import WIDTH, HEIGHT


class TestViewFunctions(unittest.TestCase):
    """
    Unit tests for view rendering functions.
    """

    def setUp(self):
        """
        Initialize Pygame and a dummy screen before each test.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.model = Model()

    def test_draw_player_does_not_crash(self):
        """
        Test that draw_player does not raise an exception.
        """
        try:
            view.draw_player(self.model.player1)
        except Exception as e:
            self.fail(f"draw_player() raised an exception: {e}")

    def tearDown(self):
        """
        Quit Pygame after each test.
        """
        pygame.quit()


if __name__ == "__main__":
    unittest.main()
