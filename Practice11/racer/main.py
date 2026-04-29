import pygame
import sys
import random
import time
import os

pygame.init()
pygame.mixer.init()

# Get the folder where this file is located.
# This helps to load images and sounds correctly from any terminal location.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")
SOUND_DIR = os.path.join(BASE_DIR, "sound")

# Screen settings
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Practice 11 Racer")

clock = pygame.time.Clock()
FPS = 75

# Main game variables
SPEED = 4
SCORE = 0
COIN_SCORE = 0
COLLECTED_COINS = 0

# Enemy speed will increase after every 5 collected coins.
SPEED_UP_EVERY = 5

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (255, 182, 193)
YELLOW = (255, 215, 0)
BLUE = (70, 160, 255)
GREEN = (80, 200, 120)
PURPLE = (160, 90, 220)
GRAY = (80, 80, 80)
RED = (220, 60, 60)

# Fonts
font_big = pygame.font.SysFont("Verdana", 40, bold=True)
font_small = pygame.font.SysFont("Verdana", 18)


# This function loads an image from the images folder.
# If the image is missing, it creates a simple colored rectangle instead.
def load_image(name, size, fallback_color):
    path = os.path.join(IMAGE_DIR, name)

    if os.path.exists(path):
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, size)

    image = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.rect(image, fallback_color, image.get_rect(), border_radius=8)
    return image


# This function loads a sound from the sound folder.
# If the sound is missing, the game will continue without crashing.
def load_sound(name):
    path = os.path.join(SOUND_DIR, name)

    if os.path.exists(path):
        return pygame.mixer.Sound(path)

    return None


# Load all game images and sounds.
background = load_image("road.png", (WIDTH, HEIGHT), GRAY)
player_img = load_image("red_car.png", (80, 100), RED)
enemy_img = load_image("white_car.png", (80, 100), WHITE)
coin_img = load_image("coin.png", (34, 34), YELLOW)
crash_sound = load_sound("crash.mp3")


# This function draws text on the screen.
def draw_text(text, x, y, color=BLACK):
    img = font_small.render(text, True, color)
    screen.blit(img, (x, y))


# This function draws the coin weight number on top of the coin.
def draw_coin_weight(coin):
    pygame.draw.circle(screen, coin.color, coin.rect.center, 20, 3)

    value = font_small.render(str(coin.weight), True, BLACK)
    value_rect = value.get_rect(center=coin.rect.center)
    screen.blit(value, value_rect)


# Player class controls the player's car.
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 80)

    # Move player left and right using keyboard arrows.
    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)

        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.move_ip(5, 0)


# Enemy class controls the enemy car.
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.reset()

    # Enemy appears at a random x position above the screen.
    def reset(self):
        self.rect.center = (random.randint(60, WIDTH - 60), -100)

    # Enemy moves down with the current SPEED.
    def move(self):
        global SCORE

        self.rect.move_ip(0, SPEED)

        if self.rect.top > HEIGHT:
            SCORE += 1
            self.reset()


# Coin class controls random coins with different weights.
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect()
        self.weight = 1
        self.color = YELLOW
        self.reset()

    # Assignment 11 requirement:
    # Coins have different random weights.
    def choose_weight(self):
        coin_types = [
            (1, YELLOW),
            (2, BLUE),
            (3, GREEN),
            (5, PURPLE)
        ]

        self.weight, self.color = random.choice(coin_types)

    # Coin appears randomly on the road.
    # It should not appear directly on the enemy car.
    def reset(self):
        self.choose_weight()

        while True:
            new_x = random.randint(50, WIDTH - 50)
            new_y = random.randint(-240, -80)

            self.rect.center = (new_x, new_y)

            coin_hitbox = self.rect.inflate(-18, -18)
            enemy_hitbox = enemy.rect.inflate(-35, -35)

            if not coin_hitbox.colliderect(enemy_hitbox):
                break

    # Coin moves down with the road speed.
    def move(self):
        self.rect.move_ip(0, SPEED)

        if self.rect.top > HEIGHT:
            self.reset()


# Create game objects.
player = Player()
enemy = Enemy()
coin = Coin()

# Store all sprites in one group.
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)
all_sprites.add(coin)

running = True

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw background.
    screen.blit(background, (0, 0))

    # Draw score information.
    draw_text(f"Cars: {SCORE}", 10, 10)
    draw_text(f"Coin score: {COIN_SCORE}", 10, 35)
    draw_text(f"Coins: {COLLECTED_COINS}", 10, 60)
    draw_text(f"Speed: {round(SPEED, 1)}", 10, 85)

    # Draw and move all sprites.
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()

    # Draw coin weight number.
    draw_coin_weight(coin)

    # Assignment 11 requirement:
    # When player collects a coin, score increases by coin weight.
    if player.rect.colliderect(coin.rect):
        COIN_SCORE += coin.weight
        COLLECTED_COINS += 1

        # Assignment 11 requirement:
        # Enemy speed increases after every N collected coins.
        if COLLECTED_COINS % SPEED_UP_EVERY == 0:
            SPEED += 1

        coin.reset()

    # Smaller hitboxes make collision more realistic.
    player_hitbox = player.rect.inflate(-20, -20)
    enemy_hitbox = enemy.rect.inflate(-20, -20)

    # If player collides with enemy, game ends.
    if player_hitbox.colliderect(enemy_hitbox):
        if crash_sound is not None:
            crash_sound.play()

        time.sleep(0.5)

        screen.fill(PINK)

        text = font_big.render("Game Over", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        screen.blit(text, text_rect)

        result = font_small.render(f"Final coin score: {COIN_SCORE}", True, WHITE)
        result_rect = result.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
        screen.blit(result, result_rect)

        pygame.display.update()
        time.sleep(2)

        running = False

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()