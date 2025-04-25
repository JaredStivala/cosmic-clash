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


# Dummy classes to enable the game to run
class DummyPlayer:
    def __init__(self, name, name1, rect, lives):
        self.name = name
        self.name1 = name1
        self.rect = rect
        self.lives = lives


class DummyGame:
    def __init__(self):
        self.player1 = DummyPlayer(
            name="Player1", name1="Player1", rect=pygame.Rect(50, 200, 50, 50), lives=3
        )
        self.player2 = DummyPlayer(
            name="Player2", name1="Player1", rect=pygame.Rect(700, 200, 50, 50), lives=3
        )
        self.bullets = []
        self.aliens = []

    def spawn_bullet(self, player_id):
        print(f"Bullet spawned by player {player_id}")

    def spawn_alien(self, x, y):
        print(f"Alien spawned at {x}, {y}")


# Drawing functions
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


def render(game):
    screen.fill(BLACK)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        game.spawn_bullet(player_id=1)
    if keys[pygame.K_LEFT]:
        game.spawn_bullet(player_id=2)

    global last_alien_spawn_time
    current_time = pygame.time.get_ticks()
    if current_time - last_alien_spawn_time > ALIEN_SPAWN_INTERVAL:
        y_pos = random.randint(0, SCREEN_HEIGHT - 40)
        game.spawn_alien(x=SCREEN_WIDTH // 2, y=y_pos)
        last_alien_spawn_time = current_time

    draw_player(game.player1)
    draw_player(game.player2)

    for bullet in game.bullets:
        draw_bullet(bullet)

    for alien in game.aliens:
        draw_alien(alien)

    draw_score(
        game.player1.lives, game.player2.lives, game.player1.name, game.player2.name
    )
    pygame.display.flip()


def quit_game():
    pygame.quit()


# Main game logic
if __name__ == "__main__":
    game = DummyGame()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        render(game)
        clock.tick(60)
    quit_game()
