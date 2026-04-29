import pygame
import random
import sys

pygame.init()

# Screen and grid settings
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BLOCK_SIZE = 20

# Food disappears after 5000 milliseconds, which means 5 seconds.
FOOD_LIFETIME = 5000

# Colors
WHITE = (255, 255, 255)
PINK = (255, 105, 180)
BLACK = (20, 20, 20)
BLUE = (135, 206, 250)
YELLOW = (255, 215, 0)
GREEN = (80, 200, 120)
PURPLE = (160, 90, 220)

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Practice 11 Snake")

clock = pygame.time.Clock()
font_style = pygame.font.SysFont("bahnschrift", 25)
small_font = pygame.font.SysFont("bahnschrift", 18)

# Assignment 11 requirement:
# Food has different random weights and different colors.
food_types = [
    {"weight": 1, "color": BLUE},
    {"weight": 2, "color": YELLOW},
    {"weight": 3, "color": GREEN},
    {"weight": 5, "color": PURPLE}
]


# This function shows score, level, food weight, and timer.
def show_score(score, level, food_weight, time_left):
    value = font_style.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(value, (10, 10))

    food_info = small_font.render(f"Food: +{food_weight}  Timer: {time_left}s", True, WHITE)
    screen.blit(food_info, (10, 40))


# This function generates food at a random grid position.
# It also chooses a random food weight.
def generate_food(snake_list):
    while True:
        food_x = random.randrange(0, SCREEN_WIDTH, BLOCK_SIZE)
        food_y = random.randrange(0, SCREEN_HEIGHT, BLOCK_SIZE)

        # Food must not appear inside the snake body.
        if [food_x, food_y] not in snake_list:
            food = random.choice(food_types)

            return {
                "x": food_x,
                "y": food_y,
                "weight": food["weight"],
                "color": food["color"],
                "spawn_time": pygame.time.get_ticks()
            }


# This function draws every segment of the snake.
def draw_snake(snake_list):
    for segment in snake_list:
        pygame.draw.rect(
            screen,
            PINK,
            (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE),
            border_radius=4
        )


# This function draws food and shows its weight number inside.
def draw_food(food):
    pygame.draw.rect(
        screen,
        food["color"],
        (food["x"], food["y"], BLOCK_SIZE, BLOCK_SIZE),
        border_radius=5
    )

    text = small_font.render(str(food["weight"]), True, BLACK)
    text_rect = text.get_rect(center=(food["x"] + BLOCK_SIZE // 2, food["y"] + BLOCK_SIZE // 2))
    screen.blit(text, text_rect)


# This function shows the game over screen.
def game_over_screen(score):
    screen.fill(BLACK)

    msg = font_style.render(f"Game Over! Score: {score}", True, PINK)
    msg_rect = msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    screen.blit(msg, msg_rect)
    pygame.display.update()
    pygame.time.delay(2000)


def game_loop():
    # Basic game variables
    fps = 7
    score = 0
    level = 1
    food_per_level = 5

    # Snake starts from the center of the screen.
    x = SCREEN_WIDTH // 2
    y = SCREEN_HEIGHT // 2

    # Snake starts moving to the right.
    x_change = BLOCK_SIZE
    y_change = 0

    # Snake body is stored as a list of coordinates.
    snake_list = [[x, y]]
    length_of_snake = 1

    # Generate the first food.
    food = generate_food(snake_list)

    running = True

    # Main game loop
    while running:
        now = pygame.time.get_ticks()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Change snake direction.
            # Opposite direction is blocked to avoid instant self-collision.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -BLOCK_SIZE
                    y_change = 0

                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = BLOCK_SIZE
                    y_change = 0

                elif event.key == pygame.K_UP and y_change == 0:
                    x_change = 0
                    y_change = -BLOCK_SIZE

                elif event.key == pygame.K_DOWN and y_change == 0:
                    x_change = 0
                    y_change = BLOCK_SIZE

        # Move snake head.
        x += x_change
        y += y_change

        # Wall collision.
        if x >= SCREEN_WIDTH or x < 0 or y >= SCREEN_HEIGHT or y < 0:
            running = False

        # Add new head position to the snake body.
        snake_head = [x, y]
        snake_list.append(snake_head)

        # Remove tail if snake length is bigger than allowed length.
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Self collision.
        for segment in snake_list[:-1]:
            if segment == snake_head:
                running = False

        # Assignment 11 requirement:
        # Food gives different score and length depending on its weight.
        if x == food["x"] and y == food["y"]:
            score += food["weight"]
            length_of_snake += food["weight"]

            # Level and speed increase after enough score.
            if score // food_per_level + 1 > level:
                level += 1
                fps += 1

            food = generate_food(snake_list)

        # Assignment 11 requirement:
        # Food disappears after some time and a new food appears.
        if now - food["spawn_time"] >= FOOD_LIFETIME:
            food = generate_food(snake_list)

        # Calculate remaining food lifetime in seconds.
        time_left = max(0, (FOOD_LIFETIME - (now - food["spawn_time"])) // 1000)

        # Draw everything.
        screen.fill(BLACK)

        draw_food(food)
        draw_snake(snake_list)
        show_score(score, level, food["weight"], time_left)

        pygame.display.update()
        clock.tick(fps)

    game_over_screen(score)


# Start the game only when this file is launched directly.
if __name__ == "__main__":
    game_loop()