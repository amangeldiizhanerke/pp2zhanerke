import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

clock = pygame.time.Clock()

color = BLACK
brush_size = 8
mode = "brush"

drawing = False
start_pos = None
last_pos = None


def draw_smooth_line(surface, color, start, end, radius):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))

    if distance == 0:
        pygame.draw.circle(surface, color, start, radius)
        return

    for i in range(distance + 1):
        x = int(start[0] + dx * i / distance)
        y = int(start[1] + dy * i / distance)
        pygame.draw.circle(surface, color, (x, y), radius)


def draw_rectangle(surface, color, start, end, width=0):
    x1, y1 = start
    x2, y2 = end
    rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
    pygame.draw.rect(surface, color, rect, width)


def draw_circle(surface, color, start, end, width=0):
    x1, y1 = start
    x2, y2 = end
    center = ((x1 + x2) // 2, (y1 + y2) // 2)
    radius = int(math.hypot(x2 - x1, y2 - y1) / 2)
    if radius > 0:
        pygame.draw.circle(surface, color, center, radius, width)


running = True
while running:
    temp_surface = canvas.copy()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_b:
                mode = "brush"
            elif event.key == pygame.K_r:
                mode = "rectangle"
            elif event.key == pygame.K_c:
                mode = "circle"
            elif event.key == pygame.K_e:
                mode = "eraser"

            elif event.key == pygame.K_1:
                color = RED
            elif event.key == pygame.K_2:
                color = GREEN
            elif event.key == pygame.K_3:
                color = BLUE
            elif event.key == pygame.K_4:
                color = YELLOW
            elif event.key == pygame.K_5:
                color = PURPLE
            elif event.key == pygame.K_6:
                color = BLACK

            elif event.key == pygame.K_UP:
                brush_size += 2
            elif event.key == pygame.K_DOWN:
                brush_size = max(2, brush_size - 2)

            elif event.key == pygame.K_z:
                canvas.fill(WHITE)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos
            last_pos = event.pos

            if mode == "brush":
                pygame.draw.circle(canvas, color, event.pos, brush_size)
            elif mode == "eraser":
                pygame.draw.circle(canvas, WHITE, event.pos, brush_size)

        elif event.type == pygame.MOUSEMOTION and drawing:
            if mode == "brush":
                draw_smooth_line(canvas, color, last_pos, event.pos, brush_size)
                last_pos = event.pos
            elif mode == "eraser":
                draw_smooth_line(canvas, WHITE, last_pos, event.pos, brush_size)
                last_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = event.pos

                if mode == "rectangle":
                    draw_rectangle(canvas, color, start_pos, end_pos)
                elif mode == "circle":
                    draw_circle(canvas, color, start_pos, end_pos)

            drawing = False
            start_pos = None
            last_pos = None

    screen.blit(canvas, (0, 0))

    if drawing and mode in ["rectangle", "circle"] and start_pos is not None:
        current_pos = pygame.mouse.get_pos()
        preview = canvas.copy()

        if mode == "rectangle":
            draw_rectangle(preview, color, start_pos, current_pos, 2)
        elif mode == "circle":
            draw_circle(preview, color, start_pos, current_pos, 2)

        screen.blit(preview, (0, 0))

    pygame.display.flip()
    clock.tick(120)

pygame.quit()