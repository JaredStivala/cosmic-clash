# controller.py

import pygame


class Controller:
    """
    A class to handle player input and control their actions in the game.

    Attributes:
        player1: An object representing the first player, which should have attributes
                 `dy` (vertical movement speed) and `shoot` (boolean indicating shooting action).
        player2: An object representing the second player, which should have attributes
                 `dy` (vertical movement speed) and `shoot` (boolean indicating shooting action).
    """

    """
        Initializes the Controller with two players.

        Args:
            player1: The first player object.
            player2: The second player object.
        """

    """
        Processes a list of input events and updates player actions accordingly.

        Args:
            events: A list of pygame events to process. Each event is expected to have
                    attributes `type` (event type) and `key` (key pressed or released).

        Behavior:
            - Player 1 controls:
                - W key: Move up.
                - S key: Move down.
                - D key: Shoot.
                - Release W or S: Stop vertical movement.
            - Player 2 controls:
                - UP arrow key: Move up.
                - DOWN arrow key: Move down.
                - LEFT arrow key: Shoot.
                - Release UP or DOWN: Stop vertical movement.
        """

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def handle_input(self, events):
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
