"""
controller.py

Handles player input and translates keyboard events into player actions.
"""

import pygame


class Controller:
    """
    A class to handle player input and control their actions in the game.

    Attributes:
        player1: An object representing the first player, with attributes like `dy` (vertical movement) and `shoot`.
        player2: An object representing the second player, with similar control attributes.
    """

    def __init__(self, player1, player2):
        """
        Initializes the Controller with two players.

        Args:
            player1: The first player object.
            player2: The second player object.
        """
        self.player1 = player1
        self.player2 = player2

    def handle_input(self, events):
        """
        Processes a list of input events and updates player actions accordingly.

        Args:
            events: A list of pygame events (e.g., KEYDOWN, KEYUP).

        Behavior:
            - Player 1 controls:
                W: Move up
                S: Move down
                D: Shoot
                Release W/S: Stop vertical movement

            - Player 2 controls:
                UP: Move up
                DOWN: Move down
                LEFT: Shoot
                Release UP/DOWN: Stop vertical movement
        """
        for event in events:
            # Player 1 controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.player1.dy = -3  # Move up
                elif event.key == pygame.K_s:
                    self.player1.dy = 3  # Move down
                elif event.key == pygame.K_d:
                    self.player1.shoot = True

            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_w, pygame.K_s):
                    self.player1.dy = 0  # Stop vertical movement

            # Player 2 controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player2.dy = -3  # Move up
                elif event.key == pygame.K_DOWN:
                    self.player2.dy = 3  # Move down
                elif event.key == pygame.K_LEFT:
                    self.player2.shoot = True

            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    self.player2.dy = 0  # Stop vertical movement
