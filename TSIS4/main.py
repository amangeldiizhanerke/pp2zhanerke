import pygame
from game import run_game, load_settings, save_settings
from db import get_leaderboard

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS4 Snake")

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (220, 220, 220)
PINK = (255, 105, 180)

font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 26)


def draw_text(text, x, y, color=BLACK):
    img = font.render(text, True, color)
    rect = img.get_rect(center=(x, y))
    screen.blit(img, rect)


def draw_small(text, x, y, color=BLACK):
    img = small_font.render(text, True, color)
    screen.blit(img, (x, y))


def button(text, x, y, w, h):
    rect = pygame.Rect(x, y, w, h)

    pygame.draw.rect(screen, GRAY, rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=10)

    img = small_font.render(text, True, BLACK)
    text_rect = img.get_rect(center=rect.center)
    screen.blit(img, text_rect)

    return rect


def play_music(settings):
#start music if enabled
    if settings["sound"]:
        try:
            pygame.mixer.music.load("assets/music.mp3")
            pygame.mixer.music.play(-1)
        except:
            pass
    else:
        pygame.mixer.music.stop()


def update_music(settings):
#apply sound setting
    if settings["sound"]:
        if not pygame.mixer.music.get_busy():
            play_music(settings)
    else:
        pygame.mixer.music.stop()


def username_screen():
    name = ""
    clock = pygame.time.Clock()

    while True:
        screen.fill(WHITE)

        draw_text("Enter username", 300, 200, PINK)
        draw_text(name + "|", 300, 270)
        draw_text("Press ENTER", 300, 340)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip() != "":
                    return name.strip()

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                else:
                    if len(name) < 12:
                        name += event.unicode

        pygame.display.flip()
        clock.tick(60)


def main_menu():
    clock = pygame.time.Clock()

    while True:
        screen.fill(WHITE)

        draw_text("Snake Game", 300, 100, PINK)

        play_btn = button("Play", 200, 190, 200, 50)
        leaderboard_btn = button("Leaderboard", 200, 260, 200, 50)
        settings_btn = button("Settings", 200, 330, 200, 50)
        quit_btn = button("Quit", 200, 400, 200, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.collidepoint(event.pos):
                    return "play"

                if leaderboard_btn.collidepoint(event.pos):
                    return "leaderboard"

                if settings_btn.collidepoint(event.pos):
                    return "settings"

                if quit_btn.collidepoint(event.pos):
                    return "quit"

        pygame.display.flip()
        clock.tick(60)


def leaderboard_screen():
    clock = pygame.time.Clock()

    while True:
        screen.fill(WHITE)

        draw_text("Leaderboard", 300, 50, PINK)
        draw_small("Rank   Username      Score   Level   Date", 60, 95)

        try:
            rows = get_leaderboard()
        except:
            rows = []

        y = 130

        if not rows:
            draw_text("No scores yet", 300, 250)
        else:
            for i, row in enumerate(rows):
                username = row[0]
                score = row[1]
                level = row[2]
                date = str(row[3])[:10]

                text = f"{i + 1:<6} {username:<12} {score:<7} {level:<7} {date}"
                draw_small(text, 60, y)
                y += 30

        back_btn = button("Back", 200, 520, 200, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    return "menu"

        pygame.display.flip()
        clock.tick(60)


def settings_screen():
    clock = pygame.time.Clock()
    settings = load_settings()

    colors = ["pink", "blue", "green"]

    while True:
        screen.fill(WHITE)

        draw_text("Settings", 300, 80, PINK)

        draw_text(f"Snake color: {settings['snake_color']}", 300, 160)
        draw_text(f"Grid: {settings['grid']}", 300, 220)
        draw_text(f"Sound: {settings['sound']}", 300, 280)

        color_btn = button("Change color", 180, 340, 240, 45)
        grid_btn = button("Grid ON/OFF", 180, 400, 240, 45)

        sound_text = "Music ON" if settings["sound"] else "Music OFF"
        sound_btn = button(sound_text, 180, 460, 240, 45)

        back_btn = button("Save & Back", 180, 520, 240, 45)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if color_btn.collidepoint(event.pos):
                    index = colors.index(settings["snake_color"])
                    settings["snake_color"] = colors[(index + 1) % len(colors)]

                elif grid_btn.collidepoint(event.pos):
                    settings["grid"] = not settings["grid"]

                elif sound_btn.collidepoint(event.pos):
                    settings["sound"] = not settings["sound"]
                    update_music(settings)

                elif back_btn.collidepoint(event.pos):
                    save_settings(settings)
                    update_music(settings)
                    return "menu"

        pygame.display.flip()
        clock.tick(60)


def game_over_screen(score, level, best):
    clock = pygame.time.Clock()

    while True:
        screen.fill(WHITE)

        draw_text("Game Over", 300, 120, PINK)
        draw_text(f"Final score: {score}", 300, 210)
        draw_text(f"Level reached: {level}", 300, 260)
        draw_text(f"Personal best: {best}", 300, 310)

        retry_btn = button("Retry", 200, 400, 200, 50)
        menu_btn = button("Main Menu", 200, 470, 200, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_btn.collidepoint(event.pos):
                    return "retry"

                if menu_btn.collidepoint(event.pos):
                    return "menu"

        pygame.display.flip()
        clock.tick(60)


def main():
    username = username_screen()

    if username is None:
        pygame.mixer.music.stop()
        pygame.quit()
        return

    settings = load_settings()
    play_music(settings)

    while True:
        action = main_menu()

        if action == "quit":
            break

        elif action == "play":
            while True:
                result, score, level, best = run_game(username)

                if result == "quit":
                    pygame.mixer.music.stop()
                    pygame.quit()
                    return

                next_action = game_over_screen(score, level, best)

                if next_action == "retry":
                    continue

                elif next_action == "menu":
                    break

                elif next_action == "quit":
                    pygame.mixer.music.stop()
                    pygame.quit()
                    return

        elif action == "leaderboard":
            result = leaderboard_screen()

            if result == "quit":
                break

        elif action == "settings":
            result = settings_screen()

            if result == "quit":
                break

    pygame.mixer.music.stop()
    pygame.quit()


if __name__ == "__main__":
    main()