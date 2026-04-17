import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BLOCK_SIZE = 20

# Colors
WHITE = (255, 255, 255)
PINK = (255, 105, 180)     # snake
BLUE = (135, 206, 250)     # food
BLACK = (20, 20, 20)       # background

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

font_style = pygame.font.SysFont("bahnschrift", 25)

def show_score(score, level):
    value = font_style.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(value, (10, 10))

def generate_food(snake_list):
    while True:
        food_x = random.randrange(0, SCREEN_WIDTH, BLOCK_SIZE)
        food_y = random.randrange(0, SCREEN_HEIGHT, BLOCK_SIZE)

        if [food_x, food_y] not in snake_list:
            return food_x, food_y

def draw_snake(snake_list):
    for segment in snake_list:
        pygame.draw.rect(screen, PINK, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

def game_over_screen(score):
    screen.fill(BLACK)
    msg = font_style.render(f"Game Over! Score: {score}", True, PINK)
    screen.blit(msg, (SCREEN_WIDTH // 5, SCREEN_HEIGHT // 3))
    pygame.display.update()
    pygame.time.delay(2000)

def game_loop():
    fps = 7  
    score = 0
    level = 1
    food_per_level = 3

    x = SCREEN_WIDTH // 2
    y = SCREEN_HEIGHT // 2

    x_change = 0
    y_change = 0

    snake_list = []
    length_of_snake = 1

    food_x, food_y = generate_food(snake_list)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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

        x += x_change
        y += y_change

        # Wall collision
        if x >= SCREEN_WIDTH or x < 0 or y >= SCREEN_HEIGHT or y < 0:
            running = False

        snake_head = [x, y]
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Self collision
        for segment in snake_list[:-1]:
            if segment == snake_head:
                running = False

        # Food collision
        if x == food_x and y == food_y:
            food_x, food_y = generate_food(snake_list)
            length_of_snake += 1
            score += 1

            if score % food_per_level == 0:
                level += 1
                fps += 1   

        screen.fill(BLACK)

        pygame.draw.rect(screen, BLUE, (food_x, food_y, BLOCK_SIZE, BLOCK_SIZE))
        draw_snake(snake_list)
        show_score(score, level)

        pygame.display.update()
        clock.tick(fps)

    game_over_screen(score)

if __name__ == "__main__":
    game_loop()