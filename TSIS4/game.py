import pygame
import random
import json
from db import save_game, get_personal_best

pygame.init()

WIDTH, HEIGHT = 600, 600
BLOCK = 20

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (220, 220, 220)
PINK = (255, 105, 180)
BLUE = (70, 150, 255)
GREEN = (80, 200, 120)
RED = (160, 0, 0)
PURPLE = (160, 90, 220)
YELLOW = (255, 220, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS4 Snake")

small_font = pygame.font.SysFont(None, 26)


def load_settings():
#load settings
    try:
        with open("settings.json", "r") as file:
            return json.load(file)
    except:
        return {
            "snake_color": "pink",
            "grid": True,
            "sound": False
        }


def save_settings(settings):
#save settings
    with open("settings.json", "w") as file:
        json.dump(settings, file, indent=4)


def get_color(name):
#snake color
    if name == "blue":
        return BLUE
    elif name == "green":
        return GREEN
    return PINK


def random_pos():
#random grid position
    return [
        random.randrange(0, WIDTH, BLOCK),
        random.randrange(0, HEIGHT, BLOCK)
    ]


def safe_pos(snake, obstacles):
#safe position
    while True:
        pos = random_pos()

        if pos not in snake and pos not in obstacles:
            return pos


def draw_grid():
#draw grid
    for x in range(0, WIDTH, BLOCK):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))

    for y in range(0, HEIGHT, BLOCK):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))


def draw_small(text, x, y, color=BLACK):
    img = small_font.render(text, True, color)
    screen.blit(img, (x, y))


def add_obstacle(snake, obstacles, food, poison):
#new obstacle from level 3
    for _ in range(100):
        pos = random_pos()

        if pos in snake:
            continue
        if pos in obstacles:
            continue
        if pos == food or pos == poison:
            continue

        head = snake[0]

        if abs(head[0] - pos[0]) <= BLOCK and abs(head[1] - pos[1]) <= BLOCK:
            continue

        obstacles.append(pos)
        break


def move_head(head, direction):
#move head
    if direction == "UP":
        head[1] -= BLOCK
    elif direction == "DOWN":
        head[1] += BLOCK
    elif direction == "LEFT":
        head[0] -= BLOCK
    elif direction == "RIGHT":
        head[0] += BLOCK

    return head


def turn_back(direction):
#opposite direction
    if direction == "UP":
        return "DOWN"
    if direction == "DOWN":
        return "UP"
    if direction == "LEFT":
        return "RIGHT"
    return "LEFT"


def is_wall_collision(head):
#check wall
    return head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT


def use_shield(snake, direction):
#safe shield turn
    snake.reverse()
    direction = turn_back(direction)
    return snake, direction


def draw_game(settings, snake, snake_color, food, poison, obstacles, powerup, power_type, username, score, level, personal_best, shield, slow, speed_boost):
#draw everything
    screen.fill(WHITE)

    if settings["grid"]:
        draw_grid()

    pygame.draw.rect(screen, GREEN, (*food, BLOCK, BLOCK))
    pygame.draw.rect(screen, RED, (*poison, BLOCK, BLOCK))

    for obs in obstacles:
        pygame.draw.rect(screen, BLACK, (*obs, BLOCK, BLOCK))

    if powerup is not None:
        if power_type == "speed":
            color = YELLOW
        elif power_type == "slow":
            color = BLUE
        else:
            color = PURPLE

        pygame.draw.rect(screen, color, (*powerup, BLOCK, BLOCK))

    for part in snake:
        pygame.draw.rect(screen, snake_color, (*part, BLOCK, BLOCK))

    draw_small(f"Player: {username}", 10, 10)
    draw_small(f"Score: {score}", 10, 35)
    draw_small(f"Level: {level}", 10, 60)
    draw_small(f"Best: {personal_best}", 10, 85)

    if shield:
        draw_small("Shield ON", 10, 110, PURPLE)

    if slow:
        draw_small("Slow", 10, 135, BLUE)

    if speed_boost:
        draw_small("Speed", 10, 160, YELLOW)

    pygame.display.flip()


def run_game(username):
    settings = load_settings()
    snake_color = get_color(settings["snake_color"])

    clock = pygame.time.Clock()

    snake = [[300, 300], [280, 300], [260, 300]]
    direction = "RIGHT"
    next_direction = "RIGHT"

    obstacles = []

    food = safe_pos(snake, obstacles)
    poison = safe_pos(snake, obstacles)

    powerup = None
    power_type = None
    power_spawn_time = 0

    score = 0
    level = 1
    speed = 8
    food_count = 0

    shield = False
    slow = False
    speed_boost = False
    effect_end = 0

    try:
        personal_best = get_personal_best(username)
    except:
        personal_best = 0

    while True:
        now = pygame.time.get_ticks()

#stop timed effects
        if now > effect_end:
            slow = False
            speed_boost = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", score, level, personal_best

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    next_direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    next_direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    next_direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    next_direction = "RIGHT"

        direction = next_direction

        head = snake[0].copy()
        head = move_head(head, direction)

#wall collision
        if is_wall_collision(head):
            if not shield:
                break

            shield = False
            snake, direction = use_shield(snake, direction)
            next_direction = direction

            draw_game(
                settings, snake, snake_color, food, poison, obstacles,
                powerup, power_type, username, score, level,
                personal_best, shield, slow, speed_boost
            )

            if slow:
                clock.tick(max(4, speed - 4))
            elif speed_boost:
                clock.tick(speed + 5)
            else:
                clock.tick(speed)

            continue

#self collision
        if head in snake:
            if not shield:
                break

            shield = False
            snake, direction = use_shield(snake, direction)
            next_direction = direction

            draw_game(
                settings, snake, snake_color, food, poison, obstacles,
                powerup, power_type, username, score, level,
                personal_best, shield, slow, speed_boost
            )

            if slow:
                clock.tick(max(4, speed - 4))
            elif speed_boost:
                clock.tick(speed + 5)
            else:
                clock.tick(speed)

            continue

        snake.insert(0, head)

#normal food
        if head == food:
            score += 1
            food_count += 1

            food = safe_pos(snake, obstacles)

            if food_count % 5 == 0:
                level += 1
                speed += 1

                if level >= 3:
                    add_obstacle(snake, obstacles, food, poison)
        else:
            snake.pop()

#poison food
        if head == poison:
            if len(snake) > 2:
                snake.pop()
                snake.pop()
            else:
                break

            if len(snake) <= 1:
                break

            poison = safe_pos(snake, obstacles)

#spawn powerup
        if powerup is None and random.randint(1, 80) == 1:
            powerup = safe_pos(snake, obstacles)
            power_type = random.choice(["speed", "slow", "shield"])
            power_spawn_time = now

#remove powerup after 8 sec
        if powerup is not None and now - power_spawn_time > 8000:
            powerup = None
            power_type = None

#take powerup
        if powerup is not None and head == powerup:
            if power_type == "speed":
                speed_boost = True
                effect_end = now + 5000

            elif power_type == "slow":
                slow = True
                effect_end = now + 5000

            elif power_type == "shield":
                shield = True

            powerup = None
            power_type = None

#obstacle collision
        if head in obstacles:
            break

        draw_game(
            settings, snake, snake_color, food, poison, obstacles,
            powerup, power_type, username, score, level,
            personal_best, shield, slow, speed_boost
        )

        if slow:
            clock.tick(max(4, speed - 4))
        elif speed_boost:
            clock.tick(speed + 5)
        else:
            clock.tick(speed)

    try:
        save_game(username, score, level)
    except:
        pass

    return "game_over", score, level, personal_best