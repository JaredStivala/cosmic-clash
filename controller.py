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
                            self.player1.dy = -5  # Move up
                        elif event.key == pygame.K_s:
                            self.player1.dy = 5  # Move down
                        elif event.key == pygame.K_d:
                            self.player1.shoot()

                    elif event.type == pygame.KEYUP:
                        if event.key in (pygame.K_w, pygame.K_s):
                            self.player1.dy = 0  # Stop vertical movement

                    # Player 2 controls
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.player2.dy = -5  # Move up
                        elif event.key == pygame.K_DOWN:
                            self.player2.dy = 5  # Move down
                        elif event.key == pygame.K_LEFT:
                            self.player2.shoot()

                    elif event.type == pygame.KEYUP:
                        if event.key in (pygame.K_UP, pygame.K_DOWN):
                            self.player2.dy = 0  # Stop vertical movement

    def _can_shoot(self, last_time):
        return pygame.time.get_ticks() - last_time > self.shot_delay
