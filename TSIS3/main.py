import pygame
from ui import main_menu, name_screen, leaderboard_screen, settings_screen, game_over_screen
from racer import run_game

pygame.init()

WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS3 Racer")


def main():
    while True:
        action = main_menu(screen)

        if action == "quit":
            break

        elif action == "play":
            player_name = name_screen(screen)

            if player_name is None:
                break

            while True:
                result, score, distance, coins = run_game(screen, player_name)

                if result == "quit":
                    pygame.quit()
                    return

                next_action = game_over_screen(screen, score, distance, coins)

                if next_action == "retry":
                    continue

                elif next_action == "menu":
                    break

                elif next_action == "quit":
                    pygame.quit()
                    return

        elif action == "leaderboard":
            result = leaderboard_screen(screen)

            if result == "quit":
                break

        elif action == "settings":
            result = settings_screen(screen)

            if result == "quit":
                break

    pygame.quit()


if __name__ == "__main__":
    main()