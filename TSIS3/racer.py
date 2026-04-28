import pygame
import random
import os
from persistence import load_settings, save_score

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 700

BLACK = (20, 20, 20)
GRAY = (100, 100, 100)
PURPLE = (160, 90, 220)

font = pygame.font.SysFont(None, 30)

ASSETS = "assets"


def load_image(name, size):
#load image
    path = os.path.join(ASSETS, name)
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, size)


def get_player_car_name(color):
#choose car image
    if color == "blue":
        return "player_car_blue.png"
    elif color == "green":
        return "player_car_green.png"
    else:
        return "player_car_pink.png"


def load_assets(settings):
#all images
    player_car = get_player_car_name(settings["car_color"])

    return {
        "road": load_image("road.png", (400, HEIGHT)),
        "player": load_image(player_car, (50, 80)),
        "enemy": load_image("enemy_car.png", (50, 80)),
        "coin": load_image("coin.png", (30, 30)),
        "obstacle": load_image("obstacle.png", (55, 40)),
        "nitro": load_image("nitro.png", (35, 35)),
        "shield": load_image("shield.png", (35, 35)),
        "repair": load_image("repair.png", (35, 35))
    }


def play_music_if_needed(settings):
#music on/off
    music_path = os.path.join(ASSETS, "music.mp3")

    if settings["sound"] and os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()


def draw_text(screen, text, x, y, color=BLACK):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def make_rect(x, y, w, h):
    return pygame.Rect(x, y, w, h)


def run_game(screen, player_name):
    settings = load_settings()
    images = load_assets(settings)
    play_music_if_needed(settings)

    difficulty = settings["difficulty"]

    if difficulty == "easy":
        base_speed = 4
        spawn_rate = 45
    elif difficulty == "hard":
        base_speed = 7
        spawn_rate = 28
    else:
        base_speed = 5
        spawn_rate = 36

    clock = pygame.time.Clock()

    player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 100, 50, 80)
    player_speed = 7

    traffic = []
    obstacles = []
    coins = []
    powerups = []

    road_y = 0

    score = 0
    coin_count = 0
    distance = 0
    finish_distance = 3000

    shield = False
    active_power = None
    power_end_time = 0

    frame = 0
    running = True

    while running:
        frame += 1
        now = pygame.time.get_ticks()

        speed = base_speed

#nitro boost
        if active_power == "nitro" and now < power_end_time:
            speed = base_speed + 4

        elif active_power == "nitro" and now >= power_end_time:
            active_power = None

        road_y += speed

        if road_y >= HEIGHT:
            road_y = 0

        distance += speed // 2

        if frame % 60 == 0:
            score += 1

#game gets harder
        extra_speed = distance // 600
        current_speed = speed + extra_speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return "quit", score, distance, coin_count

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.left > 110:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < WIDTH - 110:
            player.x += player_speed

        lanes = [150, 230, 310, 390]

#spawn cars
        if frame % spawn_rate == 0:
            x = random.choice(lanes)

            if abs(x - player.x) > 40:
                traffic.append(make_rect(x, -90, 50, 80))

#spawn obstacles
        if frame % max(35, 75 - extra_speed * 3) == 0:
            x = random.choice(lanes)

            if abs(x - player.x) > 40:
                obstacles.append(make_rect(x, -40, 55, 40))

#spawn coins
        if frame % 55 == 0:
            x = random.choice(lanes)
            coins.append(make_rect(x + 10, -30, 30, 30))

#spawn powerups
        if frame % 180 == 0:
            x = random.choice(lanes)
            kind = random.choice(["nitro", "shield", "repair"])

            powerups.append({
                "rect": make_rect(x + 5, -45, 45, 45),
                "type": kind,
                "spawn_time": now
            })

        for car in traffic:
            car.y += current_speed

        for obstacle in obstacles:
            obstacle.y += current_speed

        for coin in coins:
            coin.y += current_speed

        for item in powerups:
            item["rect"].y += current_speed

        traffic = [car for car in traffic if car.y < HEIGHT + 100]
        obstacles = [obs for obs in obstacles if obs.y < HEIGHT + 100]
        coins = [coin for coin in coins if coin.y < HEIGHT + 100]

        powerups = [
            item for item in powerups
            if item["rect"].y < HEIGHT + 100 and now - item["spawn_time"] < 8000
        ]

#collect coins
        for coin in coins[:]:
            coin_hitbox = coin.inflate(25, 25)

            if player.colliderect(coin_hitbox):
                coins.remove(coin)
                coin_count += 1
                score += 10

#powerups
        for item in powerups[:]:
            power_hitbox = item["rect"].inflate(45, 45)

            if player.colliderect(power_hitbox):
                powerups.remove(item)

                if item["type"] == "repair":
                    if obstacles:
                        obstacles.pop(0)
                    score += 20
                    print("repair collected, score:", score)

                elif active_power is None:
                    if item["type"] == "nitro":
                        active_power = "nitro"
                        power_end_time = now + 4000

                    elif item["type"] == "shield":
                        active_power = "shield"
                        shield = True

#crash with car
        for car in traffic[:]:
            car_hitbox = car.inflate(-8, -8)

            if player.colliderect(car_hitbox):
                if shield:
                    traffic.remove(car)
                    shield = False
                    active_power = None
                else:
                    running = False

#crash with obstacle
        for obs in obstacles[:]:
            obstacle_hitbox = obs.inflate(60, 60)

            if player.colliderect(obstacle_hitbox):
                if shield:
                    obstacles.remove(obs)
                    shield = False
                    active_power = None
                else:
                    score -= 15
                    obstacles.remove(obs)
                    print("obstacle hit, score:", score)

        if distance >= finish_distance:
            running = False

        screen.fill(GRAY)

        screen.blit(images["road"], (100, road_y))
        screen.blit(images["road"], (100, road_y - HEIGHT))

        screen.blit(images["player"], player)

        for car in traffic:
            screen.blit(images["enemy"], car)

        for obs in obstacles:
            screen.blit(images["obstacle"], obs)

        for coin in coins:
            screen.blit(images["coin"], coin)

        for item in powerups:
            image = pygame.transform.scale(images[item["type"]], (45, 45))
            screen.blit(image, item["rect"])

        if shield:
            pygame.draw.rect(screen, PURPLE, player.inflate(12, 12), 3)

        draw_text(screen, f"Player: {player_name}", 10, 10)
        draw_text(screen, f"Score: {score}", 10, 40)
        draw_text(screen, f"Coins: {coin_count}", 10, 70)
        draw_text(screen, f"Distance: {distance}/{finish_distance}", 10, 100)

        if active_power == "nitro":
            time_left = max(0, (power_end_time - now) // 1000)
            draw_text(screen, f"Power: nitro {time_left}s", 10, 130)

        elif active_power == "shield":
            draw_text(screen, "Power: shield", 10, 130)

        if shield:
            draw_text(screen, "Shield ON", 10, 160)

        pygame.display.flip()
        clock.tick(60)

    pygame.mixer.music.stop()
    save_score(player_name, score, distance)
    return "game_over", score, distance, coin_count