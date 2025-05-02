# model.py
# This file contains the Model class and its associated classes for the game.
# It handles player and alien movements, bullet firing, and collision detection.
# It also manages the game state, including player health and score.
# pylint: disable=no-member,undefined-variable

import random
import pygame
from settings import HEIGHT, WIDTH

sound_enabled = True
try:
    pygame.mixer.init()
except pygame.error:
    print("Audio initialization failed. Sounds will be disabled.")
    sound_enabled = False

if sound_enabled:
    alien_hit = pygame.mixer.Sound("assets/alienhit.wav")
    life_loss = pygame.mixer.Sound("assets/lifeloss.wav")
else:
    alien_hit = None  # or a mock object if needed
    life_loss = None  # or a mock object if needed


class Player:
    """
    Player class representing each player in the game.
    Each player has an ID, position, health, score, and shooting capabilities.

    Attributes:
        player_id (int): Unique identifier for the player (1 or 2).
        image (pygame.Surface): Image representing the player.
        x (int): X-coordinate of the player.
        y (int): Y-coordinate of the player.
        health (int): Health points of the player.
        score (int): Score of the player.
        alive (bool): Indicates if the player is alive.
        dy (int): Change in Y-coordinate for movement.
        shot_delay (int): Delay between shots in milliseconds.
        last_shot_time (int): Timestamp of the last shot.
        shoot (bool): Indicates if the player is shooting.

    Methods:
        move(): Updates the player's position based on dy.
        can_shoot(): Checks if the player can shoot based on shot delay.
        shoot_bullet(): Creates a bullet if the player can shoot.
        get_health(): Returns the player's health.
        get_score(): Returns the player's score.
        get_alive(): Returns if the player is alive.
        lose_life(): Decreases the player's health by 1. If health is 0, sets alive to False.
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
        self.shot_delay = 200  # milliseconds
        self.last_shot_time = 0
        self.shoot = False

    def move(self):
        """
        Updates the player's position based on dy.
        The player can move up or down, but not into the hearts area.
        """
        self.y += self.dy
        self.y = max(100, min(self.y, HEIGHT - 30))  # Prevent moving into hearts area

    def can_shoot(self):
        """
        Checks if the player can shoot based on shot delay.
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
        Creates a bullet if the player can shoot.
        Returns:
            Bullet: A new Bullet object if the player can shoot, None otherwise.
        """
        if self.can_shoot():
            return Bullet(self, self.player_id)
        return None

    def get_health(self):
        """
        Returns:
            int: The player's health.
        """
        return self.health

    def get_score(self):
        """
        Returns:
            int: The player's score.
        """
        return self.score

    def get_alive(self):
        """
        Returns:
            bool: True if the player is alive, False otherwise.
        """
        return self.alive

    def lose_life(self):
        """
        Decreases the player's health by 1. If health is 0, sets alive to False.
        """
        self.health -= 1
        if self.health <= 0:
            self.alive = False


class Alien:
    """
    Alien class representing the alien enemy in the game.
    Each alien has an image, position, speed, health, and state (alive or dead).
    Attributes:
        original_image (pygame.Surface): Original image of the alien.
        image (pygame.Surface): Current image of the alien with opacity based on health.
        x (int): X-coordinate of the alien.
        y (int): Y-coordinate of the alien.
        speed_x (int): Speed of the alien in the X direction.
        health (int): Health points of the alien.
        alive (bool): Indicates if the alien is alive.
    Methods:
        update_opacity(): Updates the opacity of the alien image based on health.
        move(): Moves the alien horizontally across the screen.
        swap_direction_x(): Reverses the alien's direction in the X axis.
        get_alive(): Returns if the alien is alive.
        lose_life(): Decreases the alien's health by 1. If health is 0, sets alive to False.
        check_collision_with_player(player1, player2): Checks for collision with players and updates their states.
    """

    def __init__(self):
        original_image = pygame.image.load("assets/alien.png").convert_alpha()
        width, height = original_image.get_size()
        scaled_width = int(width * 0.75)
        scaled_height = int(height * 0.75)
        self.original_image = pygame.transform.smoothscale(
            original_image, (scaled_width, scaled_height)
        )

        self.image = self.original_image.copy()
        self.x = WIDTH // 2
        self.y = random.randint(80, HEIGHT - 30)
        self.speed_x = 2 if random.choice([True, False]) else -2
        self.health = 3
        self.alive = True
        self.update_opacity()  # set initial opacity

    def update_opacity(self):
        """
        Updates the opacity of the alien image based on its health.
        The opacity is scaled from 0 to 255 based on the health value.
        Health 3 -> 255, 2 -> ~170, 1 -> ~85
        """
        # Scale alpha by health: 3 -> 255, 2 -> ~170, 1 -> ~85
        alpha = int((self.health / 3) * 255)
        self.image = self.original_image.copy()
        self.image.set_alpha(alpha)

    def move(self):
        """
        Moves the alien horizontally across the screen.
        If the alien reaches the screen edges, it reverses direction.
        """
        self.x += self.speed_x
        if self.x <= 0 or self.x >= WIDTH:
            self.swap_direction_x()

    def swap_direction_x(self):
        """
        Reverses the alien's direction in the X axis.
        """
        self.speed_x = -self.speed_x
        self.x += self.speed_x

    def get_alive(self):
        """
        Returns:
            bool: True if the alien is alive, False otherwise.
        """
        return self.alive

    def lose_life(self):
        """
        Decreases the alien's health by 1. If health is 0, sets alive to False.
        If the alien is hit, it bounces back and reduces opacity.
        """
        self.health -= 1
        if self.health <= 0:
            self.alive = False
            if sound_enabled:
                alien_hit.play()
        else:
            self.swap_direction_x()  # bounce
            self.update_opacity()  # reduce opacity
            if sound_enabled:
                alien_hit.play()

    def check_collision_with_player(self, player1, player2):
        """
        Checks for collision with players and updates their states.
        If the alien collides with a player, the player loses a life and the alien is removed.
        Args:
            player1 (Player): The first player.
            player2 (Player): The second player.
        """
        if abs(self.x - player1.x) < 30:
            player1.lose_life()
            player2.score += 1
            self.alive = False
            if sound_enabled:
                life_loss.play()

        elif abs(self.x - player2.x) < 30:
            player2.lose_life()
            player1.score += 1
            self.alive = False
            if sound_enabled:
                life_loss.play()


class Bullet:
    """
    Bullet class representing the bullets fired by players.
    Each bullet has an image, position, speed, and state (alive or not).
    Attributes:
        image (pygame.Surface): Image representing the bullet.
        x (int): X-coordinate of the bullet.
        y (int): Y-coordinate of the bullet.
        speed (int): Speed of the bullet.
        alive (bool): Indicates if the bullet is alive.
    Methods:
        move(): Moves the bullet horizontally across the screen.
        get_position(): Returns the current position of the bullet.
        is_off_screen(): Checks if the bullet is off-screen.
    """

    def __init__(self, player, player_id):
        self.image = pygame.image.load("assets/bullets.png").convert_alpha()
        self.x = int(player.x)
        self.y = int(player.y)
        self.speed = 10 if player_id == 1 else -10
        self.alive = True

    def move(self):
        """
        Moves the bullet horizontally across the screen.
        If the bullet goes off-screen, it is marked as not alive.
        """
        self.x += self.speed

    def get_position(self):
        """
        Returns:
            tuple: The current position of the bullet (x, y).
        """
        return (self.x, self.y)

    def is_off_screen(self):
        """
        Checks if the bullet is off-screen.
        Returns:
            bool: True if the bullet is off-screen, False otherwise.
        """
        return self.x < 0 or self.x > WIDTH


class Model:
    """
    Model class representing the game state, including players, aliens, and bullets.
    Attributes:
        player1 (Player): The first player.
        player2 (Player): The second player.
        aliens (list): List of aliens in the game.
        bullets (list): List of bullets in the game.
        last_alien_spawn_time (int): Timestamp of the last alien spawn.
        alien_spawn_interval (int): Time interval for spawning aliens.
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
        Adds a bullet to the game if the player can shoot.
        Args:
            player_id (int): The ID of the player (1 or 2) who is shooting.
        """
        bullet = (
            self.player1.shoot_bullet()
            if player_id == 1
            else self.player2.shoot_bullet()
        )
        if bullet:
            self.bullets.append(bullet)

    def remove_bullet(self, bullet):
        """
        Removes a bullet from the game if it goes off-screen.
        Args:
            bullet (Bullet): The bullet to be removed.
        """
        # Remove the bullet from the list if it goes off-screen
        if bullet in self.bullets:
            self.bullets.remove(bullet)

    def spawn_alien(self):
        """
        Spawns a new alien at a random Y position within the screen height.
        The alien moves horizontally across the screen.
        """
        new_alien = Alien()
        self.aliens.append(new_alien)

    def update(self):
        """
        Update the game state, including player movement, bullet movement,
        alien movement, and collision detection.
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
                if abs(bullet.x - alien.x) < 30 and abs(bullet.y - alien.y) < 30:
                    alien.lose_life()  # Bounce (X) on 1st and 2nd hit, dies on 3rd hit
                    self.remove_bullet(bullet)  # Bullet always disappears after hit
                    break  # Move to next bullet

        # Move aliens and check collisions with players
        for alien in self.aliens[:]:
            alien.move()
            alien.check_collision_with_player(self.player1, self.player2)
            if not alien.get_alive():
                self.aliens.remove(alien)
