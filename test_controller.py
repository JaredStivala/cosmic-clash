"""
test_controller.py

Unit tests for the Controller class in controller.py.
Tests check whether input events correctly update player states.
"""

# pylint: disable=no-member,undefined-variable

import unittest
import pygame
import pygame.locals as pl
from controller import Controller
from model import Model


class TestController(unittest.TestCase):
    """
    Unit tests for the Controller class.
    """

    def setUp(self):
        """
        Initialize Pygame, display, model, and controller before each test.
        """
        pygame.init()
        pygame.display.set_mode((800, 600))  # Needed for image conversion
        self.model = Model()
        self.controller = Controller(self.model.player1, self.model.player2)

    def test_handle_input_player1_shoots(self):
        """
        Test that player1's shoot flag is set when D is pressed.
        """
        event = pygame.event.Event(pl.KEYDOWN, {"key": pl.K_d})
        self.controller.handle_input([event])
        self.assertTrue(self.model.player1.shoot)

    def test_handle_input_player2_moves_up(self):
        """
        Test that player2 moves up when UP key is pressed.
        """
        event = pygame.event.Event(pl.KEYDOWN, {"key": pl.K_UP})
        self.controller.handle_input([event])
        self.assertLess(self.model.player2.dy, 0)

    def tearDown(self):
        """
        Quit Pygame after each test.
        """
        pygame.quit()


if __name__ == "__main__":
    unittest.main()
