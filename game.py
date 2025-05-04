"""
game.py

Main entry point for the Cosmic Clash game. Handles game setup, screens, input,
audio initialization, and the main game loop. Uses Model, Controller, and view
modules to render and control the game state.

Functions:
    wrap_text(text, font, max_width): Wraps long text into multiple lines.
    initial_rules_screen(): Displays the game rules.
    name_input_screen(): Allows users to enter their player names.
    countdown_screen(): Displays a countdown before the game starts.
    end_screen(winner_name): Displays the winning message and replay prompt.
    main(): Runs the entire game loop and handles transitions.
"""

# pylint: disable=no-member,undefined-variable

import pygame
from controller import Controller
from model import Model
import view

pygame.init()
clock = pygame.time.Clock()
font_large = pygame.font.SysFont(None, 72)
font_medium = pygame.font.SysFont(None, 48)

sound_enabled = True
try:
    pygame.mixer.init()
except pygame.error:  # pylint-disable
    print("Audio initialization failed. Sounds will be disabled.")
    sound_enabled = False

if sound_enabled:
    bullet_shoot = pygame.mixer.Sound("assets/bulletshoot.wav")
else:
    bullet_shoot = None


def wrap_text(text, font, max_width):
    """
    Splits the given text into multiple lines so that each line fits within the specified max width.

    Args:
        text (str): The text to wrap.
        font (pygame.font.Font): The font used to measure text width.
        max_width (int): Maximum pixel width for each line.

    Returns:
        list: A list of string lines wrapped to fit the screen.
    """
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    lines.append(current_line.strip())
    return lines


def initial_rules_screen():
    """
    Displays the initial rules screen explaining game mechanics and controls.
    Waits for the player to press ENTER to proceed.
    """
    running = True

    font_large = pygame.font.SysFont(None, int(view.SCREEN_HEIGHT * 0.08))
    font_medium = pygame.font.SysFont(None, int(view.SCREEN_HEIGHT * 0.045))

    objective_text = [
        "OBJECTIVE:",
        "- Don't let the aliens pass you.",
        "- Protect your side of the screen.",
        "- The first player to reach 3 points wins the match.",
    ]

    how_to_score_text = [
        "HOW TO SCORE:",
        "- You score 1 point when an alien passes your opponent’s side.",
        "- Aliens move horizontally across the screen.",
        "- Shoot them to reverse their direction.",
        "- If an alien is hit by a bullet:",
        "  - First and second hit: it reverses direction (horizontal bounce).",
        "  - Third hit: it disappears from the game.",
    ]

    controls_text = [
        "CONTROLS:",
        "Player 1 (LEFT)   | Move: W / S    , Shoot: D",
        "Player 2 (RIGHT)  | Move: UP / DOWN    , Shoot: LEFT",
    ]
    continue_text = "Press ENTER to continue."

    while running:
        view.screen.fill((0, 0, 0))
        title = font_large.render("COSMIC CLASH — GAME RULES", True, (255, 255, 0))
        view.screen.blit(
            title,
            (
                view.SCREEN_WIDTH // 2 - title.get_width() // 2,
                int(view.SCREEN_HEIGHT * 0.03),
            ),
        )

        top_margin = int(view.SCREEN_HEIGHT * 0.15)
        side_margin = int(view.SCREEN_WIDTH * 0.05)
        column_spacing = int(view.SCREEN_WIDTH * 0.1)
        column_width = (view.SCREEN_WIDTH - 2 * side_margin - column_spacing) // 2
        line_spacing = int(view.SCREEN_HEIGHT * 0.045)

        y_offset_left = top_margin
        x_left = side_margin
        for line in objective_text:
            color = (255, 255, 255) if line.isupper() else (200, 200, 200)
            wrapped_lines = wrap_text(line, font_medium, column_width)
            for wrapped_line in wrapped_lines:
                rendered_line = font_medium.render(wrapped_line, True, color)
                view.screen.blit(rendered_line, (x_left, y_offset_left))
                y_offset_left += line_spacing

        y_offset_right = top_margin
        x_right = side_margin + column_width + column_spacing
        for line in how_to_score_text:
            color = (255, 255, 255) if line.isupper() else (200, 200, 200)
            wrapped_lines = wrap_text(line, font_medium, column_width)
            for wrapped_line in wrapped_lines:
                rendered_line = font_medium.render(wrapped_line, True, color)
                view.screen.blit(rendered_line, (x_right, y_offset_right))
                y_offset_right += line_spacing

        y_offset_bottom = view.SCREEN_HEIGHT - int(view.SCREEN_HEIGHT * 0.25)
        for line in controls_text:
            rendered_line = font_medium.render(
                line, True, (255, 255, 255) if line.isupper() else (200, 200, 200)
            )
            view.screen.blit(
                rendered_line,
                (
                    view.SCREEN_WIDTH // 2 - rendered_line.get_width() // 2,
                    y_offset_bottom,
                ),
            )
            y_offset_bottom += line_spacing

        y_offset_bottom += int(line_spacing * 0.8)
        continue_rendered = font_medium.render(continue_text, True, (255, 255, 255))
        view.screen.blit(
            continue_rendered,
            (
                view.SCREEN_WIDTH // 2 - continue_rendered.get_width() // 2,
                y_offset_bottom,
            ),
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False


def name_input_screen():
    """
    Prompts each player to enter their name. Handles keyboard input including backspace and Enter.

    Returns:
        tuple: Names of player 1 and player 2 as strings.
    """
    player_names = ["", ""]
    current_player = 0
    input_active = True

    while input_active:
        view.screen.fill((0, 0, 0))
        prompt = font_medium.render(
            f"Enter name for Player {current_player + 1}:", True, (255, 255, 255)
        )
        name_display = font_large.render(
            player_names[current_player], True, (255, 255, 0)
        )
        continue_text = font_medium.render(
            "Press ENTER when done", True, (200, 200, 200)
        )

        view.screen.blit(
            prompt, (view.SCREEN_WIDTH // 2 - prompt.get_width() // 2, 150)
        )
        view.screen.blit(
            name_display, (view.SCREEN_WIDTH // 2 - name_display.get_width() // 2, 250)
        )
        view.screen.blit(
            continue_text,
            (view.SCREEN_WIDTH // 2 - continue_text.get_width() // 2, 400),
        )
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if player_names[current_player] != "":
                        current_player += 1
                        if current_player > 1:
                            input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    player_names[current_player] = player_names[current_player][:-1]
                else:
                    if len(player_names[current_player]) < 12:
                        player_names[current_player] += event.unicode

    return player_names[0], player_names[1]


def countdown_screen():
    """
    Displays a countdown from 3 to 1 before the match starts, with 1-second intervals.
    """
    for count in range(3, 0, -1):
        view.screen.fill((0, 0, 0))
        text = font_large.render(str(count), True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(view.SCREEN_WIDTH // 2, view.SCREEN_HEIGHT // 2)
        )
        view.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(1000)


def end_screen(winner_name):
    """
    Displays the end screen with the winner's name and prompts to restart the game.

    Args:
        winner_name (str): Name of the player who won.
    """
    view.screen.fill((0, 0, 0))
    end_text = font_large.render(
        f"End of the Game! {winner_name} won!", True, (255, 0, 0)
    )
    end_rect = end_text.get_rect(
        center=(view.SCREEN_WIDTH // 2, view.SCREEN_HEIGHT // 2 - 50)
    )
    view.screen.blit(end_text, end_rect)

    restart_text = font_medium.render("Tap Enter to Play Again", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(
        center=(view.SCREEN_WIDTH // 2, view.SCREEN_HEIGHT // 2 + 50)
    )
    view.screen.blit(restart_text, restart_rect)

    pygame.display.flip()


def main():
    """
    Main game loop. Manages the flow from welcome screen to gameplay to ending.
    Handles player movement, bullet firing, alien spawning, collisions, score tracking, and game reset.
    """
    while True:
        initial_rules_screen()
        player1_name, player2_name = name_input_screen()
        countdown_screen()

        model = Model()
        controller = Controller(model.player1, model.player2)
        running = True
        game_over = False

        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            controller.handle_input(events)

            model.player1.move()
            model.player2.move()

            if model.player1.shoot:
                model.add_bullet(player_id=1)
                if sound_enabled:
                    bullet_shoot.play()
                model.player1.shoot = False
            if model.player2.shoot:
                model.add_bullet(player_id=2)
                if sound_enabled:
                    bullet_shoot.play()
                model.player2.shoot = False

            model.update()

            if model.player1.score >= 3:
                winner_name = player1_name
                game_over = True
            elif model.player2.score >= 3:
                winner_name = player2_name
                game_over = True

            view.render(model, player1_name, player2_name)
            clock.tick(60)

            if game_over:
                running = False

        end_screen(winner_name)

        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting_for_restart = False


if __name__ == "__main__":
    main()
