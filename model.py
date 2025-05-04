"""
model.py

This module defines the game logic and core entities for the 2D shooting game.
It includes classes for Player, Alien, Bullet, and the central Model that manages state.

Classes:
    Player: Represents a player character with movement and shooting abilities.
    Alien: Represents an enemy that moves and can collide with players.
    Bullet: Represents a projectile shot by a player.
    Model: Represents the game state and contains update logic.
"""

import random
import pygame
from settings import HEIGHT, WIDTH


class Player:
    """
    Player class representing each player in the game.
    Each player has an ID, position, health, score, and shooting capabilities.
    """

    def __init__(self, player_id):
        self.player_id = player_id
        self.image = pygame.image.load(f"assets/player{player_id}.png").convert_alpha()
        self.x = 50 if player_id == 1 else WIDTH - 50
        self.y = HEIGHT // 2
        self.health = 3
        self.score = 0
        self.alive = True
        self.dy = 0
        self.shot_delay = 300  # milliseconds
        self.last_shot_time = 0
        self.shoot = False

    def move(self):
        """
        Move the player vertically based on the current dy value.
        The player cannot move into the hearts area at the bottom of the screen.
        """
        self.y += self.dy
        self.y = max(80, min(self.y, HEIGHT - 30))  # Prevent moving into hearts area

    def can_shoot(self):
        """
        Check if the player can shoot based on the shot delay.
        Returns:
            bool: True if the player can shoot, False otherwise.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shot_delay:
            self.last_shot_time = current_time
            return True
        return False

    def shoot_bullet(self):
        """
        Create a new bullet if the player can shoot.
        Returns:
            Bullet: A new Bullet instance if the player can shoot, None otherwise.
        """
        if self.can_shoot():
            return Bullet(self, self.player_id)
        return None

    def get_health(self):
        """
        Get the current health of the player.
        Returns:
            int: The current health of the player.
        """
        return self.health

    def get_score(self):
        """
        Get the current score of the player.
        Returns:
            int: The current score of the player.
        """
        return self.score

    def get_alive(self):
        """
        Check if the player is alive.
        Returns:
            bool: True if the player is alive, False otherwise.
        """
        return self.alive

    def lose_life(self):
        """
        Decrease the player's health by 1. If health reaches 0, set alive to False.
        """
        self.health -= 1
        if self.health <= 0:
            self.alive = False


class Alien:
    """
    Alien class representing an enemy alien in the game.

    Attributes:
        x (int): X-coordinate of the alien.
        y (int): Y-coordinate of the alien.
        health (int): Remaining health of the alien.
        alive (bool): Whether the alien is still active.
        rect (pygame.Rect): Rect for collision detection.
        direction_x (int): Horizontal movement direction.
        opacity (int): Transparency level for visual effects.
    """

    def __init__(self):
        original_image = pygame.image.load("assets/alien.png").convert_alpha()
        width, height = original_image.get_size()
        scaled_width = int(width * 0.75)
        scaled_height = int(height * 0.75)
        self.image = pygame.transform.smoothscale(
            original_image, (scaled_width, scaled_height)
        )

        self.x = WIDTH // 2
        self.y = random.randint(80, HEIGHT - 30)
        self.speed_x = 2 if random.choice([True, False]) else -2
        self.health = 3
        self.alive = True

    def move(self):
        """
        Move the alien horizontally based on its speed.
        If it hits the screen edges, it bounces back.
        """
        self.x += self.speed_x
        if self.x <= 0 or self.x >= WIDTH:
            self.swap_direction_x()

    def swap_direction_x(self):
        """
        Reverse the horizontal direction of the alien.
        """
        self.speed_x = -self.speed_x
        self.x += self.speed_x

    def get_alive(self):
        """
        Check if the alien is alive.
        Returns:
            bool: True if the alien is alive, False otherwise.
        """
        return self.alive

    def lose_life(self):
        """
        Decrease the alien's health by 1. If health reaches 0, set alive to False.
        On the first and second hits, it bounces horizontally.
        """
        self.health -= 1
        if self.health <= 0:
            self.alive = False
        else:
            self.swap_direction_x()  # Bounce horizontally on first and second hits

    def check_collision_with_player(self, player1, player2):
        """
        Check for collision with players. If a player is hit, they lose a life.
        If the alien is hit, it loses a life.
        Args:
            player1 (Player): First player instance.
            player2 (Player): Second player instance.
        1. If the alien collides with player1, player1 loses a life and player2 scores.
        2. If the alien collides with player2, player2 loses a life and player1 scores.
        3. If the alien is hit by a bullet, it loses a life and the bullet is removed.
        4. If the alien's health reaches 0, it is marked as not alive.
        """
        if abs(self.x - player1.x) < 30:
            player1.lose_life()
            player2.score += 1
            self.alive = False
        elif abs(self.x - player2.x) < 30:
            player2.lose_life()
            player1.score += 1
            self.alive = False


class Bullet:
    """
    Bullet class representing a projectile fired by a player.

    Attributes:
        x (int): X-coordinate of the bullet.
        y (int): Y-coordinate of the bullet.
        speed (int): Horizontal speed of the bullet.
        alive (bool): Whether the bullet is still active.
    """

    def __init__(self, player, player_id):
        self.image = pygame.image.load("assets/bullets.png").convert_alpha()
        self.x = int(player.x)
        self.y = int(player.y)
        self.speed = 10 if player_id == 1 else -10
        self.alive = True

    def move(self):
        """
        Move the bullet horizontally based on its speed.
        """
        self.x += self.speed

    def get_position(self):
        """
        Get the current position of the bullet.
        Returns:
            tuple: (x, y) coordinates of the bullet.
        """
        return (self.x, self.y)

    def is_off_screen(self):
        """
        Check if the bullet is off the screen.
        Returns:
            bool: True if the bullet is off the screen, False otherwise.
        """
        return self.x < 0 or self.x > WIDTH


class Model:
    """
    Model class representing the overall game state.

    Manages players, aliens, bullets, and collision logic.

    Attributes:
        player1 (Player): First player instance.
        player2 (Player): Second player instance.
        aliens (list): List of active Alien instances.
        bullets (list): List of active Bullet instances.
    """

    def __init__(self):
        self.player1 = Player(1)
        self.player2 = Player(2)
        self.aliens = []
        self.bullets = []
        self.last_alien_spawn_time = pygame.time.get_ticks()
        self.alien_spawn_interval = 1500  # More frequent alien spawn

    def add_bullet(self, player_id):
        """
        Add a bullet to the game based on the player ID.
        Args:
            player_id (int): ID of the player who is shooting."""
        bullet = (
            self.player1.shoot_bullet()
            if player_id == 1
            else self.player2.shoot_bullet()
        )
        if bullet:
            self.bullets.append(bullet)

    def remove_bullet(self, bullet):
        """
        Remove a bullet from the game.
        Args:
            bullet (Bullet): The bullet instance to remove.
        """
        if bullet in self.bullets:
            self.bullets.remove(bullet)

    def spawn_alien(self):
        """
        Spawn a new alien at a random vertical position.
        The alien's horizontal speed is randomly set to either 2 or -2.
        """
        new_alien = Alien()
        self.aliens.append(new_alien)

    def update(self):
        """
        Update the game state, including player movement, bullet movement,
        alien spawning, and collision detection.
        """
        # Spawn aliens
        current_time = pygame.time.get_ticks()
        if current_time - self.last_alien_spawn_time > self.alien_spawn_interval:
            self.spawn_alien()
            self.last_alien_spawn_time = current_time

        # Move players
        self.player1.move()
        self.player2.move()

        # Move bullets and remove off-screen ones
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.is_off_screen():
                self.remove_bullet(bullet)

        # Bullet–Alien collision logic
        for bullet in self.bullets[:]:
            for alien in self.aliens[:]:
                if abs(bullet.x - alien.x) < 20 and abs(bullet.y - alien.y) < 20:
                    alien.lose_life()  # Bounce (X) on 1st and 2nd hit, dies on 3rd hit
                    self.remove_bullet(bullet)  # Bullet always disappears after hit
                    break  # Move to next bullet

        # Move aliens and check collisions with players
        for alien in self.aliens[:]:
            alien.move()
            alien.check_collision_with_player(self.player1, self.player2)
            if not alien.get_alive():
                self.aliens.remove(alien)
