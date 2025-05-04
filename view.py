"""
view.py

Handles all rendering logic for Cosmic Clash. This includes drawing players, bullets, aliens,
backgrounds, health indicators, and scores on the screen. All Pygame screen blitting and
graphic manipulation is centralized here.

Functions:
    draw_player(player): Renders the given player to the screen.
    draw_bullet(bullet): Renders a bullet object.
    draw_alien(alien): Renders an alien object.
    draw_lives(health, x, y): Draws green/red heart icons based on player health.
    draw_score(player1, player2, name1, name2): Displays names and remaining lives.
    render(model, name1, name2): Central rendering function combining all elements.
    quit_game(): Exits the game and closes Pygame.
"""

# pylint: disable=no-member,undefined-variable

import pygame
from settings import WIDTH, HEIGHT

pygame.init()

SCREEN_WIDTH = WIDTH
SCREEN_HEIGHT = HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cosmic Clash")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Load images
player1_img = pygame.image.load("assets/player1.png").convert_alpha()
player2_img = pygame.image.load("assets/player2.png").convert_alpha()
alien_img = pygame.image.load("assets/alien.png").convert_alpha()
background_img = pygame.image.load("assets/space.jpg").convert()
green_heart_img = pygame.image.load("assets/greenh.png").convert_alpha()
red_heart_img = pygame.image.load("assets/redh.png").convert_alpha()
bullet_img = pygame.image.load("assets/bullets.png").convert_alpha()


def draw_player(player):
    """
    Renders the player's spaceship on the screen with appropriate scaling and position.

    Args:
        player (Player): The player object containing position and ID.
    """
    img = player1_img if player.player_id == 1 else player2_img
    scaled_img = pygame.transform.scale(img, (50, 50))
    rect = scaled_img.get_rect(center=(int(player.x), int(player.y)))
    screen.blit(scaled_img, rect)


def draw_bullet(bullet):
    """
    Renders a bullet on the screen with correct position and orientation.

    Args:
        bullet (Bullet): The bullet object with x, y coordinates.
    """
    scaled_bullet = pygame.transform.scale(bullet_img, (20, 10))
    rect = scaled_bullet.get_rect(center=(int(bullet.x), int(bullet.y)))
    screen.blit(scaled_bullet, rect)


def draw_alien(alien):
    """
    Renders an alien using its image and position.

    Args:
        alien (Alien): The alien object to render.
    """
    scaled_alien = pygame.transform.scale(alien.image, (60, 60))
    rect = scaled_alien.get_rect(center=(int(alien.x), int(alien.y)))
    screen.blit(scaled_alien, rect)


def draw_lives(health, x, y):
    """
    Draws the player's remaining health using heart icons.

    Args:
        health (int): Current health (0 to 3).
        x (int): X-position to start drawing.
        y (int): Y-position to draw the hearts.
    """
    heart_size = 30
    for i in range(3):
        heart_img = green_heart_img if i < health else red_heart_img
        screen.blit(
            pygame.transform.scale(heart_img, (heart_size, heart_size)),
            (x + i * (heart_size + 5), y),
        )


def draw_score(player1, player2, name1, name2):
    """
    Renders each player's name and corresponding heart health indicators.

    Args:
        player1 (Player): Player 1 instance.
        player2 (Player): Player 2 instance.
        name1 (str): Player 1 name.
        name2 (str): Player 2 name.
    """
    text1 = font.render(name1, True, (255, 255, 255))
    text2 = font.render(name2, True, (255, 255, 255))
    screen.blit(text1, (10, 10))
    draw_lives(player1.get_health(), 10, 50)
    screen.blit(text2, (SCREEN_WIDTH - 150, 10))
    draw_lives(player2.get_health(), SCREEN_WIDTH - 150, 50)


def render(model, name1, name2):
    """
    Master rendering function called each frame to update the screen.

    Args:
        model (Model): The current game state.
        name1 (str): Name of player 1.
        name2 (str): Name of player 2.
    """
    screen.blit(
        pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0)
    )

    draw_player(model.player1)
    draw_player(model.player2)

    for bullet in model.bullets:
        draw_bullet(bullet)

    for alien in model.aliens:
        if alien.get_alive():
            draw_alien(alien)

    draw_score(model.player1, model.player2, name1, name2)

    pygame.display.flip()


def quit_game():
    """
    Cleanly quits the game and closes the Pygame window.
    """
    pygame.quit()
