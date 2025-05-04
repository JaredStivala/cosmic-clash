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

import pygame
import random
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
        self.y += self.dy
        self.y = max(80, min(self.y, HEIGHT - 30))  # Prevent moving into hearts area

    def can_shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shot_delay:
            self.last_shot_time = current_time
            return True
        return False

    def shoot_bullet(self):
        if self.can_shoot():
            return Bullet(self, self.player_id)
        return None

    def get_health(self):
        return self.health

    def get_score(self):
        return self.score

    def get_alive(self):
        return self.alive

    def lose_life(self):
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
        self.x += self.speed_x
        if self.x <= 0 or self.x >= WIDTH:
            self.swap_direction_x()

    def swap_direction_x(self):
        self.speed_x = -self.speed_x
        self.x += self.speed_x

    def get_alive(self):
        return self.alive

    def lose_life(self):
        self.health -= 1
        if self.health <= 0:
            self.alive = False
        else:
            self.swap_direction_x()  # Bounce horizontally on first and second hits

    def check_collision_with_player(self, player1, player2):
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
        self.x += self.speed

    def get_position(self):
        return (self.x, self.y)

    def is_off_screen(self):
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
        bullet = (
            self.player1.shoot_bullet()
            if player_id == 1
            else self.player2.shoot_bullet()
        )
        if bullet:
            self.bullets.append(bullet)

    def remove_bullet(self, bullet):
        if bullet in self.bullets:
            self.bullets.remove(bullet)

    def spawn_alien(self):
        new_alien = Alien()
        self.aliens.append(new_alien)

    def update(self):
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
