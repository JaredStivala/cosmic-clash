import pygame


class Controller:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.shot_delay = 300  # milliseconds
        self.last_shot_time_p1 = 0
        self.last_shot_time_p2 = 0


def handle_input(self, keys):
    # Player 1 controls
    if keys[pygame.K_w]:
        self.player1.move_up()
    if keys[pygame.K_s]:
        self.player1.move_down()
    if keys[pygame.K_d]:
        if self._can_shoot(self.last_shot_time_p1):
            self.player1.shoot()
            self.last_shot_time_p1 = pygame.time.get_ticks()

    # Player 2 Controls
    if keys[pygame.K_UP]:
        self.player2.move_up()
    if keys[pygame.K_DOWN]:
        self.player2.move_down()
    if keys[pygame.K_LEFT]:
        if self._can_shoot(self.last_shot_time_p2):
            self.player2.shoot()
            self.last_shot_time_p2 = pygame.time.get_ticks()


def _can_shoot(self, last_time):
    return pygame.time.get_ticks() - last_time > self.shot_delay
