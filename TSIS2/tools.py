import pygame


PENCIL = "pencil"
LINE = "line"
RECT = "rect"
CIRCLE = "circle"
SQUARE = "square"
RIGHT_TRIANGLE = "right_triangle"
EQUILATERAL_TRIANGLE = "equilateral_triangle"
RHOMBUS = "rhombus"
FILL = "fill"
TEXT = "text"
ERASER = "eraser"


def draw_pencil(surface, color, start_pos, end_pos, size):
#free draw
    pygame.draw.line(surface, color, start_pos, end_pos, size)


def draw_line(surface, color, start_pos, end_pos, size):
#line
    pygame.draw.line(surface, color, start_pos, end_pos, size)


def draw_rect(surface, color, start_pos, end_pos, size):
#rectangle
    x1, y1 = start_pos
    x2, y2 = end_pos

    rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
    pygame.draw.rect(surface, color, rect, size)


def draw_square(surface, color, start_pos, end_pos, size):
#square
    x1, y1 = start_pos
    x2, y2 = end_pos

    side = min(abs(x2 - x1), abs(y2 - y1))

    if x2 < x1:
        x1 -= side
    if y2 < y1:
        y1 -= side

    rect = pygame.Rect(x1, y1, side, side)
    pygame.draw.rect(surface, color, rect, size)


def draw_circle(surface, color, start_pos, end_pos, size):
#circle
    x1, y1 = start_pos
    x2, y2 = end_pos

    radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
    pygame.draw.circle(surface, color, start_pos, radius, size)


def draw_right_triangle(surface, color, start_pos, end_pos, size):
#right triangle
    x1, y1 = start_pos
    x2, y2 = end_pos

    points = [(x1, y1), (x1, y2), (x2, y2)]
    pygame.draw.polygon(surface, color, points, size)


def draw_equilateral_triangle(surface, color, start_pos, end_pos, size):
#equilateral triangle
    x1, y1 = start_pos
    x2, y2 = end_pos

    width = x2 - x1
    height = abs(width) * 0.86

    if y2 < y1:
        height = -height

    points = [
        (x1, y2),
        (x2, y2),
        ((x1 + x2) // 2, y2 - height)
    ]

    pygame.draw.polygon(surface, color, points, size)


def draw_rhombus(surface, color, start_pos, end_pos, size):
#rhombus
    x1, y1 = start_pos
    x2, y2 = end_pos

    mid_x = (x1 + x2) // 2
    mid_y = (y1 + y2) // 2

    points = [
        (mid_x, y1),
        (x2, mid_y),
        (mid_x, y2),
        (x1, mid_y)
    ]

    pygame.draw.polygon(surface, color, points, size)


def flood_fill(surface, start_pos, fill_color):
#fill area
    width, height = surface.get_size()

    if start_pos[0] < 0 or start_pos[0] >= width:
        return
    if start_pos[1] < 0 or start_pos[1] >= height:
        return

    target_color = surface.get_at(start_pos)

    if target_color == fill_color:
        return

    stack = [start_pos]

    while stack:
        x, y = stack.pop()

        if x < 0 or x >= width or y < 0 or y >= height:
            continue

        if surface.get_at((x, y)) != target_color:
            continue

        surface.set_at((x, y), fill_color)

        stack.append((x + 1, y))
        stack.append((x - 1, y))
        stack.append((x, y + 1))
        stack.append((x, y - 1))