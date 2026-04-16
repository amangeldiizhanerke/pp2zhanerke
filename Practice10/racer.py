import pygame
import sys
import random
import time
import os

pygame.init()
pygame.mixer.init()

# Screen settings
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")

clock = pygame.time.Clock()
FPS = 75

# Game variables
SPEED = 4
SCORE = 0
COINS = 0

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (255, 182, 193)

# Fonts
font_big = pygame.font.SysFont("Verdana", 40, bold=True)
font_small = pygame.font.SysFont("Verdana", 20)

# Load images
background = pygame.image.load(os.path.join("images", "road.png"))
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

player_img = pygame.image.load(os.path.join("images", "red_car.png")).convert_alpha()
player_img = pygame.transform.scale(player_img, (80, 100))

enemy_img = pygame.image.load(os.path.join("images", "white_car.png")).convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (80, 100))

coin_img = pygame.image.load(os.path.join("images", "coin.png")).convert_alpha()
coin_img = pygame.transform.scale(coin_img, (30, 30))

crash_sound = pygame.mixer.Sound(os.path.join("sound", "crash.mp3"))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 80)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)

        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.move_ip(5, 0)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.center = (random.randint(60, WIDTH - 60), -100)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)

        if self.rect.top > HEIGHT:
            SCORE += 1
            self.reset()


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        # Монета появляется отдельно, выше экрана
        # и не ставится прямо поверх enemy
        while True:
            new_x = random.randint(50, WIDTH - 50)
            new_y = random.randint(-220, -80)

            self.rect.center = (new_x, new_y)

            # Проверяем, чтобы монета не лежала прямо на машине enemy
            # Небольшое пересечение допустимо, но не полное наложение
            overlap_rect = self.rect.inflate(-18, -18)
            enemy_check_rect = enemy.rect.inflate(-35, -35)

            if not overlap_rect.colliderect(enemy_check_rect):
                break

    def move(self):
        self.rect.move_ip(0, SPEED)

        if self.rect.top > HEIGHT:
            self.reset()


# Create objects
player = Player()
enemy = Enemy()
coin = Coin()

# Groups
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)
all_sprites.add(coin)

coins_group = pygame.sprite.Group()
coins_group.add(coin)

# Speed increase event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == INC_SPEED:
            SPEED += 0.1

    # Draw background
    screen.blit(background, (0, 0))

    # Draw counters
    score_text = font_small.render(f"Cars: {SCORE}", True, BLACK)
    coin_text = font_small.render(f"Coins: {COINS}", True, BLACK)

    screen.blit(score_text, (10, 10))
    screen.blit(coin_text, (WIDTH - 120, 10))

    # Move and draw sprites
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()

    # Coin collision
    if pygame.sprite.spritecollide(player, coins_group, False):
        COINS += 1
        coin.reset()

    # Enemy collision
    if player.rect.inflate(-20, -20).colliderect(enemy.rect.inflate(-20, -20)):
        crash_sound.play()
        time.sleep(0.5)

        screen.fill(PINK)

        text = font_big.render("Game Over", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

        pygame.display.update()
        time.sleep(2)

        running = False

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()