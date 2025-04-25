# Cosmic Clash Model]

import pygame
from settings import HEIGHT, WIDTH


class Player:
    """Class representing a player in the game.
    Attributes:
        image (pygame.Surface): The image representing the player.
        x (int): The x-coordinate of the player.
        y (int): The y-coordinate of the player.
        health (int): The health of the player.
        score (int): The score of the player.
        alive (bool): Whether the player is alive or not.

    Methods:
        move(dy): Move the player up or down by dy pixels.
        get_position(): Return the current position of the player.
        get_health(): Return the current health of the player.
        get_score(): Return the current score of the player.
        get_alive(): Return the alive status of the player.
        lose_life(): Reduce the player's health by one and check if they are still alive.
    """

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
        """Move the player up or down by dy pixels."""
        self.y += dy

    def get_position(self):
        """Return the current position of the player."""
        return (self.x, self.y)

    def get_health(self):
        """Return the current health of the player."""
        return self.health

    def get_score(self):
        """Return the current score of the player."""
        return self.score

    def get_alive(self):
        """Return the alive status of the player."""
        return self.alive

    def lose_life(self):
        """Reduce the player's health by one and check if they are still alive."""
        self.health -= 1
        if self.health <= 0:
            self.alive = False
        return self.alive


class Alien:
    """Class representing an alien in the game.
    Attributes:
        image (pygame.Surface): The image representing the alien.
        x (int): The x-coordinate of the alien.
        y (int): The y-coordinate of the alien.
        speed (int): The speed of the alien.
        alive (bool): Whether the alien is alive or not.

    Methods:
        move(dx, dy): Move the alien by dx pixels horizontally and dy pixels vertically.
        get_position(): Return the current position of the alien.
        get_alive(): Return the alive status of the alien.
    """

    def __init__(
        self,
    ):
        self.image = pygame.image.load("alien.png")
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.speed = 5
        self.health = 5
        self.alive = True

    def move(self, dx):
        """Move the alien by dx pixels horizontally and dy pixels vertically."""
        self.x += dx

    def get_position(self):
        """Return the current position of the alien."""
        return (self.x, self.y)

    def get_alive(self):
        """Return the alive status of the alien."""
        return self.alive

    def lose_life(self):
        """Reduce the alien's health by one and check if they are still alive."""
        self.health -= 1
        if self.health <= 0:
            self.alive = False
        return self.alive

    def swap_direction(self):
        """Swap the direction of the alien."""
        self.speed = -self.speed
        self.x += self.speed


class Bullet:
    """Class representing a bullet in the game.
    Attributes:
        image (pygame.Surface): The image representing the bullet.
        x (int): The x-coordinate of the bullet.
        y (int): The y-coordinate of the bullet.
        speed (int): The speed of the bullet.
        alive (bool): Whether the bullet is alive or not.

    Methods:
        move(dx, dy): Move the bullet by dx pixels horizontally and dy pixels vertically.
        get_position(): Return the current position of the bullet.
        get_alive(): Return the alive status of the bullet.
    """

    def __init__(self, player, player_id):
        self.image = pygame.image.load("bullet.png")
        self.x = player.x
        self.y = player.y

        if player_id == 1:
            self.speed = 10
        else:
            self.speed = -10
        self.alive = True

    def move(self, dx):
        """Move the bullet by dx pixels horizontally and dy pixels vertically."""
        self.x += dx


class GameState:
    """Class representing the game state.
    Attributes:
        player1 (Player): The first player.
        player2 (Player): The second player.
        alien (Alien): The alien in the game.
        bullets (list): List of bullets in the game.

    Methods:
        add_bullet(player_id): Add a bullet for the specified player.
        get_bullets(): Return the list of bullets.
    """

    def __init__(self):
        self.player1 = Player(1)
        self.player2 = Player(2)
        self.alien = Alien()
        self.bullets = []

    def add_bullet(self, player_id):
        """Add a bullet for the specified player."""
        if player_id == 1:
            bullet = Bullet(self.player1, player_id)
        else:
            bullet = Bullet(self.player2, player_id)
        self.bullets.append(bullet)
        return bullet
    
    def get_bullets(self):
        """Return the list of bullets."""
        return self.bullets
    
    def remove_bullet(self, bullet):
        """Remove a bullet from the list."""
        if bullet in self.bullets:
            self.bullets.remove(bullet)
        
    def update(self, )
