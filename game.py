# game.py

import pygame
from controller import Controller
from model import Model
import view

pygame.init()
clock = pygame.time.Clock()
font_large = pygame.font.SysFont(None, 72)
font_medium = pygame.font.SysFont(None, 48)


def wrap_text(text, font, max_width):
    """
    Splits text into lines so that each line does not exceed max_width.
    Returns a list of lines.
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
    running = True

    # Fonts
    font_large = pygame.font.SysFont(None, int(view.SCREEN_HEIGHT * 0.08))
    font_medium = pygame.font.SysFont(None, int(view.SCREEN_HEIGHT * 0.045))

    # Content
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
        "Player 1 | Move: W / S    , Shoot: D",
        "Player 2 | Move: UP / DOWN    , Shoot: LEFT",
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

        # LEFT COLUMN — OBJECTIVE (with wrapping)
        y_offset_left = top_margin
        x_left = side_margin
        for line in objective_text:
            color = (255, 255, 255) if line.isupper() else (200, 200, 200)
            wrapped_lines = wrap_text(line, font_medium, column_width)
            for wrapped_line in wrapped_lines:
                rendered_line = font_medium.render(wrapped_line, True, color)
                view.screen.blit(rendered_line, (x_left, y_offset_left))
                y_offset_left += line_spacing

        # RIGHT COLUMN — HOW TO SCORE (with wrapping)
        y_offset_right = top_margin
        x_right = side_margin + column_width + column_spacing
        for line in how_to_score_text:
            color = (255, 255, 255) if line.isupper() else (200, 200, 200)
            wrapped_lines = wrap_text(line, font_medium, column_width)
            for wrapped_line in wrapped_lines:
                rendered_line = font_medium.render(wrapped_line, True, color)
                view.screen.blit(rendered_line, (x_right, y_offset_right))
                y_offset_right += line_spacing

        # BOTTOM — CONTROLS (aligned)
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

        # Extra space before "Press ENTER"
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
                    # Otherwise, wait for the name
                elif event.key == pygame.K_BACKSPACE:
                    player_names[current_player] = player_names[current_player][:-1]
                else:
                    if len(player_names[current_player]) < 12:
                        player_names[current_player] += event.unicode

    return player_names[0], player_names[1]


def countdown_screen():
    for count in range(3, 0, -1):
        view.screen.fill((0, 0, 0))
        text = font_large.render(str(count), True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(view.SCREEN_WIDTH // 2, view.SCREEN_HEIGHT // 2)
        )
        view.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(1000)  # 1 second between numbers


def end_screen(winner_name):
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
    while True:  # Game restart loop
        # Show initial screens
        initial_rules_screen()
        player1_name, player2_name = name_input_screen()
        countdown_screen()

        # Game setup
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

            # Handle input
            controller.handle_input(events)

            # Update game state
            model.player1.move()
            model.player2.move()

            if model.player1.shoot:
                model.add_bullet(player_id=1)
                model.player1.shoot = False
            if model.player2.shoot:
                model.add_bullet(player_id=2)
                model.player2.shoot = False

            model.update()

            # Check for game over (score of 3)
            if model.player1.score >= 3:
                winner_name = player1_name
                game_over = True
            elif model.player2.score >= 3:
                winner_name = player2_name
                game_over = True

            # Render game with player names
            view.render(model, player1_name, player2_name)
            clock.tick(60)

            if game_over:
                running = False

        # End screen
        end_screen(winner_name)

        # Wait for Enter to restart
        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting_for_restart = False  # Restart the game


if __name__ == "__main__":
    main()
