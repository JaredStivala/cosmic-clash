# Cosmic Clash Model]

import pygame
from settings import HEIGHT, WIDTH, FPS


class player:
    def __init__(self, player_id):
        if player_id == 1:
            self.image = pygame.image.load("player1.png")
            self.x = 10
        else:
            self.image = pygame.image.load("player2.png")
            self.x = WIDTH - 10
        self.y = HEIGHT / 2
        self.health = 3
        self.score = 0
        self.alive = True

    def move(self, dy):
        self.y += dy

    def get_position(self):
        return (self.x, self.y)
