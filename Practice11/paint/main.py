import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Practice 11 Paint")

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


# draw smooth brush line
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


# draw rectangle from start point to end point
def draw_rectangle(surface, color, start, end, width=0):
    x1, y1 = start
    x2, y2 = end
    rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
    pygame.draw.rect(surface, color, rect, width)


# draw circle inside selected area
def draw_circle(surface, color, start, end, width=0):
    x1, y1 = start
    x2, y2 = end
    center = ((x1 + x2) // 2, (y1 + y2) // 2)
    radius = int(math.hypot(x2 - x1, y2 - y1) / 2)

    if radius > 0:
        pygame.draw.circle(surface, color, center, radius, width)


# draw square with equal width and height
def draw_square(surface, color, start, end, width=0):
    x1, y1 = start
    x2, y2 = end

    dx = x2 - x1
    dy = y2 - y1
    side = min(abs(dx), abs(dy))

    if dx < 0:
        x = x1 - side
    else:
        x = x1

    if dy < 0:
        y = y1 - side
    else:
        y = y1

    rect = pygame.Rect(x, y, side, side)
    pygame.draw.rect(surface, color, rect, width)


# draw right triangle
def draw_right_triangle(surface, color, start, end, width=0):
    points = [
        start,
        (end[0], start[1]),
        end
    ]

    pygame.draw.polygon(surface, color, points, width)


# draw equilateral triangle
def draw_equilateral_triangle(surface, color, start, end, width=0):
    x1, y1 = start
    x2, y2 = end

    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2

    dx = x2 - x1
    dy = y2 - y1

    height = math.sqrt(3) / 2

    third_x = mid_x - dy * height
    third_y = mid_y + dx * height

    points = [
        (x1, y1),
        (x2, y2),
        (third_x, third_y)
    ]

    pygame.draw.polygon(surface, color, points, width)


# draw rhombus inside selected area
def draw_rhombus(surface, color, start, end, width=0):
    x1, y1 = start
    x2, y2 = end

    left = min(x1, x2)
    right = max(x1, x2)
    top = min(y1, y2)
    bottom = max(y1, y2)

    center_x = (left + right) // 2
    center_y = (top + bottom) // 2

    points = [
        (center_x, top),
        (right, center_y),
        (center_x, bottom),
        (left, center_y)
    ]

    pygame.draw.polygon(surface, color, points, width)


# choose which shape to draw
def draw_shape(surface, color, start, end, width=0):
    if mode == "rectangle":
        draw_rectangle(surface, color, start, end, width)

    elif mode == "circle":
        draw_circle(surface, color, start, end, width)

    elif mode == "square":
        draw_square(surface, color, start, end, width)

    elif mode == "right_triangle":
        draw_right_triangle(surface, color, start, end, width)

    elif mode == "equilateral_triangle":
        draw_equilateral_triangle(surface, color, start, end, width)

    elif mode == "rhombus":
        draw_rhombus(surface, color, start, end, width)


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            # choose drawing tools
            elif event.key == pygame.K_b:
                mode = "brush"

            elif event.key == pygame.K_r:
                mode = "rectangle"

            elif event.key == pygame.K_c:
                mode = "circle"

            elif event.key == pygame.K_e:
                mode = "eraser"

            elif event.key == pygame.K_s:
                mode = "square"

            elif event.key == pygame.K_t:
                mode = "right_triangle"

            elif event.key == pygame.K_q:
                mode = "equilateral_triangle"

            elif event.key == pygame.K_h:
                mode = "rhombus"

            # choose color
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

            # change brush size
            elif event.key == pygame.K_UP:
                brush_size += 2

            elif event.key == pygame.K_DOWN:
                brush_size = max(2, brush_size - 2)

            # clear canvas
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

                if mode not in ["brush", "eraser"]:
                    draw_shape(canvas, color, start_pos, end_pos)

            drawing = False
            start_pos = None
            last_pos = None

    screen.blit(canvas, (0, 0))

    # show shape preview while mouse is dragged
    if drawing and mode not in ["brush", "eraser"] and start_pos is not None:
        current_pos = pygame.mouse.get_pos()
        preview = canvas.copy()

        draw_shape(preview, color, start_pos, current_pos, 2)

        screen.blit(preview, (0, 0))

    pygame.display.flip()
    clock.tick(120)

pygame.quit()