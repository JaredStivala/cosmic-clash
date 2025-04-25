import pygame
import random
from settings import WIDTH, HEIGHT
 
# Initialize Pygame
pygame.init()
 
# Screen dimensions
SCREEN_WIDTH = WIDTH
SCREEN_HEIGHT = HEIGHT
 
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
 
# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong x Space Invaders")
 
# Clock for controlling frame rate
clock = pygame.time.Clock()
 
# Font setup
font = pygame.font.SysFont(None, 36)
input_font = pygame.font.SysFont(None, 48)
 
# Alien spawn timer
ALIEN_SPAWN_INTERVAL = 3000  # milliseconds
last_alien_spawn_time = pygame.time.get_ticks()
 
# Load images
player1_img = pygame.image.load("assets/player1.png").convert_alpha()
player2_img = pygame.image.load("assets/player2.png").convert_alpha()
alien_img = pygame.image.load("assets/alien.png").convert_alpha()
 
 
def draw_player(player):
    if player.name == "":
        pygame.draw.rect(screen, BLUE, player.rect)
    else:
        img = player1_img if player.name == player.name1 else player2_img
        screen.blit(
            pygame.transform.scale(img, (player.rect.width, player.rect.height)),
            player.rect,
        )
 
 
def draw_bullet(bullet):
    pygame.draw.rect(screen, RED, bullet.rect)
 
 
def draw_alien(alien):
    screen.blit(
        pygame.transform.scale(alien_img, (alien.rect.width, alien.rect.height)),
        alien.rect,
    )
 
 
def draw_score(score1, score2, name1, name2):
    text1 = font.render(f"{name1}: {score1} lives", True, WHITE)
    text2 = font.render(f"{name2}: {score2} lives", True, WHITE)
    screen.blit(text1, (10, 10))
    screen.blit(text2, (SCREEN_WIDTH - 300, 10))
 
 
def render_home_screen(input_boxes, active_box_idx):
    screen.fill(BLACK)
    title = input_font.render("Enter Player Names", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
 
    labels = ["Player 1:", "Player 2:"]
    for i, box in enumerate(input_boxes):
        label = font.render(labels[i], True, WHITE)
        screen.blit(label, (SCREEN_WIDTH // 2 - 200, 200 + i * 100))
        pygame.draw.rect(screen, WHITE if i == active_box_idx else BLUE, box, 2)
 
    pygame.display.flip()
 
 
def render(game):
    """
    Render the game view based on the current game state.
    """
    screen.fill(BLACK)
 
    # Handle bullet creation from key events
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        game.spawn_bullet(player_id=1)
    if keys[pygame.K_LEFT]:
        game.spawn_bullet(player_id=2)
 
    # Handle alien creation every X seconds
    global last_alien_spawn_time
    current_time = pygame.time.get_ticks()
    if current_time - last_alien_spawn_time > ALIEN_SPAWN_INTERVAL:
        y_pos = random.randint(0, SCREEN_HEIGHT - 40)
        game.spawn_alien(x=SCREEN_WIDTH // 2, y=y_pos)
        last_alien_spawn_time = current_time
 
    # Draw players
    draw_player(game.player1)
    draw_player(game.player2)
 
    # Draw bullets
    for bullet in game.bullets:
        draw_bullet(bullet)
 
    # Draw aliens
    for alien in game.aliens:
        draw_alien(alien)
 
    # Draw scores/lives with player names
    draw_score(
        game.player1.lives, game.player2.lives, game.player1.name, game.player2.name
    )
 
    # Update display
    pygame.display.flip()
 
 
# Quit pygame (to be called on exit in main loop)
def quit_game():
    pygame.quit()
