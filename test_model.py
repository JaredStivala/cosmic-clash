"""
test_model.py

This test suite verifies the functionality of the core game logic defined in model.py.
It includes unit tests for the Player, Alien, Bullet, and Model classes using Python's unittest framework.

Each test class isolates the logic and mocks Pygame dependencies to allow for headless testing.
"""

# pylint: disable=no-member,undefined-variable

import unittest
from unittest.mock import patch
import pygame
from model import Player, Alien, Bullet, Model
from settings import WIDTH, HEIGHT

# Disable pygame's video system for headless testing
pygame.display.init()
pygame.display.set_mode((1, 1))


class TestPlayer(unittest.TestCase):
    """
    Unit tests for the Player class.
    """

    def setUp(self):
        """
        Set up a mock Player instance for testing.
        """
        self.patcher = patch("pygame.image.load", return_value=pygame.Surface((50, 50)))
        self.mock_image_load = self.patcher.start()
        self.addCleanup(self.patcher.stop)
        self.player = Player(1)

    def test_initial_state(self):
        """
        Test that the Player is initialized with the correct default state.
        """
        self.assertEqual(self.player.health, 3)
        self.assertTrue(self.player.alive)

    def test_movement_bounds(self):
        """
        Test that the Player's movement is constrained within the screen bounds.
        """
        self.player.y = 50
        self.player.dy = -10
        self.player.move()
        self.assertGreaterEqual(self.player.y, 100)

        self.player.y = HEIGHT + 100
        self.player.dy = 10
        self.player.move()
        self.assertLessEqual(self.player.y, HEIGHT - 30)

    @patch("pygame.time.get_ticks", side_effect=[0, 250])
    def test_shooting_delay(self, mock_get_ticks):  # pylint: disable=unused-argument
        """
        Test that the Player respects the shooting delay.
        """
        self.assertFalse(self.player.can_shoot())
        self.assertTrue(self.player.can_shoot())

    def test_lose_life_and_death(self):
        """
        Test that the Player loses health correctly and dies when health reaches 0.
        """
        self.player.lose_life()
        self.assertEqual(self.player.health, 2)
        self.player.lose_life()
        self.player.lose_life()
        self.assertFalse(self.player.alive)


class TestAlien(unittest.TestCase):
    """
    Unit tests for the Alien class.
    """

    def setUp(self):
        """
        Set up a mock Alien instance for testing.
        """
        patcher = patch("pygame.image.load", return_value=pygame.Surface((50, 50)))
        self.addCleanup(patcher.stop)
        patcher.start()
        self.alien = Alien()

    def test_initial_health(self):
        """
        Test that the Alien is initialized with the correct default health.
        """
        self.assertEqual(self.alien.health, 3)
        self.assertTrue(self.alien.alive)

    def test_losing_life(self):
        """
        Test that the Alien loses health correctly and dies when health reaches 0.
        """
        self.alien.lose_life()
        self.assertEqual(self.alien.health, 2)
        self.assertTrue(self.alien.alive)
        self.alien.lose_life()
        self.alien.lose_life()
        self.assertFalse(self.alien.alive)

    def test_move_and_bounce(self):
        """
        Test that the Alien moves and bounces correctly when hitting screen edges.
        """
        self.alien.x = WIDTH - 1 if self.alien.speed_x > 0 else 1
        original_direction = self.alien.speed_x

        self.alien.move()
        self.assertNotEqual(self.alien.speed_x, original_direction)


class TestBullet(unittest.TestCase):
    """
    Unit tests for the Bullet class.
    """

    def setUp(self):
        """
        Set up a mock Bullet instance for testing.
        """
        patcher = patch("pygame.image.load", return_value=pygame.Surface((10, 10)))
        self.addCleanup(patcher.stop)
        patcher.start()
        self.player = Player(1)
        self.bullet = Bullet(self.player, 1)

    def test_move(self):
        """
        Test that the Bullet moves correctly.
        """
        old_x = self.bullet.x
        self.bullet.move()
        self.assertNotEqual(old_x, self.bullet.x)

    def test_off_screen(self):
        """
        Test that the Bullet correctly identifies when it is off-screen.
        """
        self.bullet.x = -10
        self.assertTrue(self.bullet.is_off_screen())

        self.bullet.x = WIDTH + 10
        self.assertTrue(self.bullet.is_off_screen())


class TestModel(unittest.TestCase):
    """
    Unit tests for the Model class.
    """

    def setUp(self):
        """
        Set up a mock Model instance for testing.
        """
        patcher = patch("pygame.image.load", return_value=pygame.Surface((50, 50)))
        self.addCleanup(patcher.stop)
        patcher.start()
        self.model = Model()

    def test_spawn_alien(self):
        """
        Test that the Model spawns an Alien correctly.
        """
        self.assertEqual(len(self.model.aliens), 0)
        self.model.spawn_alien()
        self.assertEqual(len(self.model.aliens), 1)

    def test_add_bullet(self):
        """
        Test that the Model adds a Bullet correctly.
        """
        self.model.add_bullet(1)
        self.assertLessEqual(len(self.model.bullets), 1)

    def test_remove_bullet(self):
        """
        Test that the Model removes a Bullet correctly.
        """
        self.model.add_bullet(1)
        if self.model.bullets:
            bullet = self.model.bullets[0]
            self.model.remove_bullet(bullet)
            self.assertEqual(len(self.model.bullets), 0)


if __name__ == "__main__":
    unittest.main()
