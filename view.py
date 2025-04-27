# view.py

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
    img = player1_img if player.player_id == 1 else player2_img
    scaled_img = pygame.transform.scale(img, (50, 50))
    rect = scaled_img.get_rect(center=(int(player.x), int(player.y)))
    screen.blit(scaled_img, rect)


def draw_bullet(bullet):
    scaled_bullet = pygame.transform.scale(bullet_img, (20, 10))
    rect = scaled_bullet.get_rect(center=(int(bullet.x), int(bullet.y)))
    screen.blit(scaled_bullet, rect)


def draw_alien(alien):
    scaled_alien = pygame.transform.scale(alien_img, (60, 60))
    rect = scaled_alien.get_rect(center=(int(alien.x), int(alien.y)))
    screen.blit(scaled_alien, rect)


def draw_lives(health, x, y):
    heart_size = 30
    for i in range(3):
        heart_img = green_heart_img if i < health else red_heart_img
        screen.blit(
            pygame.transform.scale(heart_img, (heart_size, heart_size)),
            (x + i * (heart_size + 5), y),
        )


def draw_score(player1, player2, name1, name2):
    text1 = font.render(name1, True, (255, 255, 255))
    text2 = font.render(name2, True, (255, 255, 255))
    screen.blit(text1, (10, 10))
    draw_lives(player1.get_health(), 10, 50)
    screen.blit(text2, (SCREEN_WIDTH - 150, 10))
    draw_lives(player2.get_health(), SCREEN_WIDTH - 150, 50)


def render(model, name1, name2):
    # Draw background
    screen.blit(
        pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0)
    )

    # Draw players
    draw_player(model.player1)
    draw_player(model.player2)

    # Draw bullets
    for bullet in model.bullets:
        draw_bullet(bullet)

    # Draw all aliens
    for alien in model.aliens:
        if alien.get_alive():
            draw_alien(alien)

    # Draw score, lives, and player names
    draw_score(model.player1, model.player2, name1, name2)

    # Update display
    pygame.display.flip()


def quit_game():
    pygame.quit()
