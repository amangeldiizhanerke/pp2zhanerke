import pygame

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class BallGame:
    def __init__(self, screen):
        self.screen = screen
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.radius = 25
        self.step = 20

    def move(self, key):
        if key == pygame.K_LEFT and self.x - self.radius - self.step >= 0:
            self.x -= self.step
        elif key == pygame.K_RIGHT and self.x + self.radius + self.step <= WIDTH:
            self.x += self.step
        elif key == pygame.K_UP and self.y - self.radius - self.step >= 0:
            self.y -= self.step
        elif key == pygame.K_DOWN and self.y + self.radius + self.step <= HEIGHT:
            self.y += self.step

    def draw(self):
        self.screen.fill(WHITE)
        pygame.draw.circle(self.screen, RED, (self.x, self.y), self.radius)