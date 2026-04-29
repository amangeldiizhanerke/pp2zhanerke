import pygame
import math
import sys

pygame.init()

# Screen settings
WIDTH = 900
HEIGHT = 650
TOOLBAR_HEIGHT = 90

# Colors
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (210, 210, 210)
DARK_GRAY = (80, 80, 80)
RED = (230, 70, 70)
GREEN = (80, 200, 120)
BLUE = (70, 160, 255)
YELLOW = (255, 215, 0)
PINK = (255, 105, 180)
PURPLE = (160, 90, 220)

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Practice 11 Paint")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# Canvas is a separate surface below the toolbar.
# All drawings are saved on this surface.
canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(WHITE)

# Current drawing settings
current_color = BLACK
current_tool = "pencil"
brush_size = 5

# Mouse drawing state
drawing = False
start_pos = None
last_pos = None

# List of available colors.
colors = [
    (BLACK, "Black"),
    (RED, "Red"),
    (GREEN, "Green"),
    (BLUE, "Blue"),
    (YELLOW, "Yellow"),
    (PINK, "Pink"),
    (PURPLE, "Purple")
]

# List of available tools.
# Assignment 11 shapes are included here.
tools = [
    ("Pencil", "pencil"),
    ("Eraser", "eraser"),
    ("Square", "square"),
    ("Right Tri", "right_triangle"),
    ("Eq Tri", "equilateral_triangle"),
    ("Rhombus", "rhombus")
]


# This function draws text on the screen.
def draw_text(text, x, y, color=BLACK):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


# Convert mouse position from full screen coordinates to canvas coordinates.
def to_canvas_pos(pos):
    return pos[0], pos[1] - TOOLBAR_HEIGHT


# This function draws the toolbar, buttons, and color palette.
def draw_toolbar():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))

    # Draw tool buttons.
    x = 10
    for name, tool in tools:
        rect = pygame.Rect(x, 10, 120, 30)

        # Selected tool is shown with white background.
        if current_tool == tool:
            pygame.draw.rect(screen, WHITE, rect, border_radius=5)
            pygame.draw.rect(screen, BLACK, rect, 2, border_radius=5)
            draw_text(name, x + 10, 17, BLACK)
        else:
            pygame.draw.rect(screen, DARK_GRAY, rect, border_radius=5)
            draw_text(name, x + 10, 17, WHITE)

        x += 130

    # Draw color buttons.
    x = 10
    y = 52

    for color, name in colors:
        rect = pygame.Rect(x, y, 35, 28)
        pygame.draw.rect(screen, color, rect, border_radius=5)

        # Selected color has a thicker border.
        if current_color == color:
            pygame.draw.rect(screen, BLACK, rect, 3, border_radius=5)
        else:
            pygame.draw.rect(screen, BLACK, rect, 1, border_radius=5)

        x += 45

    draw_text("C - clear | ESC - quit", 350, 58, BLACK)


# This function checks which toolbar button was clicked.
def handle_toolbar_click(pos):
    global current_tool, current_color

    # Check tool buttons.
    x = 10
    for name, tool in tools:
        rect = pygame.Rect(x, 10, 120, 30)

        if rect.collidepoint(pos):
            current_tool = tool
            return

        x += 130

    # Check color buttons.
    x = 10
    y = 52

    for color, name in colors:
        rect = pygame.Rect(x, y, 35, 28)

        if rect.collidepoint(pos):
            current_color = color
            return

        x += 45


# Assignment 11 requirement:
# This function creates a square.
def get_square_rect(start, end):
    dx = end[0] - start[0]
    dy = end[1] - start[1]

    # Square width and height must be equal.
    side = min(abs(dx), abs(dy))

    if dx < 0:
        x = start[0] - side
    else:
        x = start[0]

    if dy < 0:
        y = start[1] - side
    else:
        y = start[1]

    return pygame.Rect(x, y, side, side)


# Assignment 11 requirement:
# This function creates a right triangle.
def get_right_triangle_points(start, end):
    return [
        start,
        (end[0], start[1]),
        end
    ]


# Assignment 11 requirement:
# This function creates an equilateral triangle.
def get_equilateral_triangle_points(start, end):
    x1, y1 = start
    x2, y2 = end

    # Find the middle point of the base.
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2

    dx = x2 - x1
    dy = y2 - y1

    # Height formula for equilateral triangle.
    height = math.sqrt(3) / 2

    # Calculate third point of the triangle.
    apex_x = mid_x - dy * height
    apex_y = mid_y + dx * height

    return [
        (x1, y1),
        (x2, y2),
        (apex_x, apex_y)
    ]


# Assignment 11 requirement:
# This function creates a rhombus.
def get_rhombus_points(start, end):
    left = min(start[0], end[0])
    right = max(start[0], end[0])
    top = min(start[1], end[1])
    bottom = max(start[1], end[1])

    center_x = (left + right) // 2
    center_y = (top + bottom) // 2

    return [
        (center_x, top),
        (right, center_y),
        (center_x, bottom),
        (left, center_y)
    ]


# This function draws the selected shape on the canvas.
def draw_shape(surface, tool, start, end, color):
    if tool == "square":
        pygame.draw.rect(surface, color, get_square_rect(start, end), 3)

    elif tool == "right_triangle":
        points = get_right_triangle_points(start, end)
        pygame.draw.polygon(surface, color, points, 3)

    elif tool == "equilateral_triangle":
        points = get_equilateral_triangle_points(start, end)
        pygame.draw.polygon(surface, color, points, 3)

    elif tool == "rhombus":
        points = get_rhombus_points(start, end)
        pygame.draw.polygon(surface, color, points, 3)


# Main program loop
while True:
    clock.tick(60)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Keyboard controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key == pygame.K_c:
                canvas.fill(WHITE)

        # Mouse click starts drawing or selects toolbar button.
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if event.pos[1] < TOOLBAR_HEIGHT:
                    handle_toolbar_click(event.pos)
                else:
                    drawing = True
                    start_pos = to_canvas_pos(event.pos)
                    last_pos = start_pos

        # Mouse movement draws pencil or eraser lines.
        if event.type == pygame.MOUSEMOTION:
            if drawing:
                current_pos = to_canvas_pos(event.pos)

                if current_tool == "pencil":
                    pygame.draw.line(canvas, current_color, last_pos, current_pos, brush_size)
                    last_pos = current_pos

                elif current_tool == "eraser":
                    pygame.draw.line(canvas, WHITE, last_pos, current_pos, brush_size * 3)
                    last_pos = current_pos

        # Mouse release finalizes the selected shape.
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                end_pos = to_canvas_pos(event.pos)

                if current_tool not in ["pencil", "eraser"]:
                    draw_shape(canvas, current_tool, start_pos, end_pos, current_color)

                drawing = False
                start_pos = None
                last_pos = None

    # Draw canvas on the screen.
    screen.fill(WHITE)
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    # Shape preview while dragging the mouse.
    if drawing and current_tool not in ["pencil", "eraser"]:
        preview = canvas.copy()
        mouse_pos = to_canvas_pos(pygame.mouse.get_pos())
        draw_shape(preview, current_tool, start_pos, mouse_pos, current_color)
        screen.blit(preview, (0, TOOLBAR_HEIGHT))

    draw_toolbar()
    pygame.display.flip()