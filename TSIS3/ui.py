import pygame
from persistence import load_leaderboard, load_settings, save_settings

pygame.init()

WIDTH, HEIGHT = 600, 700
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (180, 180, 180)
PINK = (255, 105, 180)

font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 28)


def draw_text(screen, text, x, y, color=BLACK, center=True):
    img = font.render(text, True, color)
    rect = img.get_rect()

    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    screen.blit(img, rect)


def draw_small_text(screen, text, x, y, color=BLACK, center=True):
    img = small_font.render(text, True, color)
    rect = img.get_rect()

    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    screen.blit(img, rect)


def button(screen, text, x, y, w, h):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, GRAY, rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=10)
    draw_text(screen, text, x + w // 2, y + h // 2)
    return rect


def name_screen(screen):
    name = ""
    clock = pygame.time.Clock()

    while True:
        screen.fill(WHITE)

        draw_text(screen, "Enter your name", WIDTH // 2, 220)
        draw_text(screen, name + "|", WIDTH // 2, 300)
        draw_small_text(screen, "Press ENTER to start", WIDTH // 2, 370)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip() != "":
                    return name

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                else:
                    if len(name) < 12:
                        name += event.unicode

        pygame.display.flip()
        clock.tick(60)


def main_menu(screen):
    clock = pygame.time.Clock()

    while True:
        screen.fill(WHITE)

        draw_text(screen, "Racer Game", WIDTH // 2, 120, PINK)

        play_btn = button(screen, "Play", 200, 220, 200, 55)
        leaderboard_btn = button(screen, "Leaderboard", 200, 295, 200, 55)
        settings_btn = button(screen, "Settings", 200, 370, 200, 55)
        quit_btn = button(screen, "Quit", 200, 445, 200, 55)

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


def leaderboard_screen(screen):
    clock = pygame.time.Clock()

    while True:
        screen.fill(WHITE)

        draw_text(screen, "Leaderboard", WIDTH // 2, 70, PINK)

        leaderboard = load_leaderboard()

        y = 140

        if not leaderboard:
            draw_text(screen, "No scores yet", WIDTH // 2, y)
        else:
            for i, item in enumerate(leaderboard):
                text = f"{i + 1}. {item['name']} | Score: {item['score']} | Dist: {item['distance']}"
                draw_small_text(screen, text, 80, y, BLACK, center=False)
                y += 35

        back_btn = button(screen, "Back", 200, 610, 200, 55)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    return "menu"

        pygame.display.flip()
        clock.tick(60)


def settings_screen(screen):
    clock = pygame.time.Clock()
    settings = load_settings()

    colors = ["pink", "blue", "green"]
    difficulties = ["easy", "normal", "hard"]

    while True:
        screen.fill(WHITE)

        draw_text(screen, "Settings", WIDTH // 2, 90, PINK)

        draw_text(screen, f"Music: {settings['sound']}", WIDTH // 2, 180)
        draw_text(screen, f"Car color: {settings['car_color']}", WIDTH // 2, 250)
        draw_text(screen, f"Difficulty: {settings['difficulty']}", WIDTH // 2, 320)

        music_text = "Music ON" if settings["sound"] else "Music OFF"

        sound_btn = button(screen, music_text, 180, 390, 240, 50)
        color_btn = button(screen, "Change color", 180, 460, 240, 50)
        diff_btn = button(screen, "Change difficulty", 180, 530, 240, 50)
        back_btn = button(screen, "Save and back", 180, 600, 240, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if sound_btn.collidepoint(event.pos):
                    settings["sound"] = not settings["sound"]

                elif color_btn.collidepoint(event.pos):
                    index = colors.index(settings["car_color"])
                    settings["car_color"] = colors[(index + 1) % len(colors)]

                elif diff_btn.collidepoint(event.pos):
                    index = difficulties.index(settings["difficulty"])
                    settings["difficulty"] = difficulties[(index + 1) % len(difficulties)]

                elif back_btn.collidepoint(event.pos):
                    save_settings(settings)
                    return "menu"

        pygame.display.flip()
        clock.tick(60)


def game_over_screen(screen, score, distance, coins):
    clock = pygame.time.Clock()

    while True:
        screen.fill(WHITE)

        draw_text(screen, "Game Over", WIDTH // 2, 150, PINK)
        draw_text(screen, f"Score: {score}", WIDTH // 2, 240)
        draw_text(screen, f"Distance: {distance}", WIDTH // 2, 290)
        draw_text(screen, f"Coins: {coins}", WIDTH // 2, 340)

        retry_btn = button(screen, "Retry", 200, 440, 200, 55)
        menu_btn = button(screen, "Main Menu", 200, 515, 200, 55)

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