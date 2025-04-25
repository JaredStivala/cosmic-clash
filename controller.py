import pygame


class Controller:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.shot_delay = 300  # milliseconds
        self.last_shot_time_p1 = 0
        self.last_shot_time_p2 = 0

    def handle_input(self, events):
        for event in events:
            # Player 1 controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.player1.move(5)  # Move up by 5 pixels
                elif event.key == pygame.K_s:
                    self.player1.move(-5)  # Move down by -5 pixels
                elif event.key == pygame.K_d:
                    if self._can_shoot(self.last_shot_time_p1):
                        self.player1.shoot()
                        self.last_shot_time_p1 = pygame.time.get_ticks()

            # Player 2 controls
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player2.move(5)  # Move up by 5 pixels
                elif event.key == pygame.K_DOWN:
                    self.player2.move(-5)  # Move down by -5 pixels
                elif event.key == pygame.K_LEFT:
                    if self._can_shoot(self.last_shot_time_p2):
                        self.player2.shoot()
                        self.last_shot_time_p2 = pygame.time.get_ticks()

    def _can_shoot(self, last_time):
        return pygame.time.get_ticks() - last_time > self.shot_delay
