# controller.py

import pygame


class Controller:
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
