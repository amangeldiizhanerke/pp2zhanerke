import pygame
import sys
from datetime import datetime
from tools import *

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint")

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
RED = (255, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 255)
PINK = (255, 105, 180)

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

clock = pygame.time.Clock()

tool = PENCIL
color = BLACK
size = 2

drawing = False
start_pos = None
last_pos = None

text_mode = False
text_pos = None
text_value = ""
font_size = 30


def save_canvas():
#save png with time
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"drawing_{now}.png"
    pygame.image.save(canvas, filename)
    print("Saved:", filename)


def draw_preview(temp_surface, current_pos):
#preview while dragging
    if start_pos is None:
        return

    if tool == LINE:
        draw_line(temp_surface, color, start_pos, current_pos, size)
    elif tool == RECT:
        draw_rect(temp_surface, color, start_pos, current_pos, size)
    elif tool == CIRCLE:
        draw_circle(temp_surface, color, start_pos, current_pos, size)
    elif tool == SQUARE:
        draw_square(temp_surface, color, start_pos, current_pos, size)
    elif tool == RIGHT_TRIANGLE:
        draw_right_triangle(temp_surface, color, start_pos, current_pos, size)
    elif tool == EQUILATERAL_TRIANGLE:
        draw_equilateral_triangle(temp_surface, color, start_pos, current_pos, size)
    elif tool == RHOMBUS:
        draw_rhombus(temp_surface, color, start_pos, current_pos, size)


def draw_final_shape(end_pos):
#save shape on canvas
    if tool == LINE:
        draw_line(canvas, color, start_pos, end_pos, size)
    elif tool == RECT:
        draw_rect(canvas, color, start_pos, end_pos, size)
    elif tool == CIRCLE:
        draw_circle(canvas, color, start_pos, end_pos, size)
    elif tool == SQUARE:
        draw_square(canvas, color, start_pos, end_pos, size)
    elif tool == RIGHT_TRIANGLE:
        draw_right_triangle(canvas, color, start_pos, end_pos, size)
    elif tool == EQUILATERAL_TRIANGLE:
        draw_equilateral_triangle(canvas, color, start_pos, end_pos, size)
    elif tool == RHOMBUS:
        draw_rhombus(canvas, color, start_pos, end_pos, size)


def draw_text_preview():
#text before enter
    if text_mode and text_pos is not None:
        font = pygame.font.SysFont(None, font_size)
        img = font.render(text_value + "|", True, color)
        screen.blit(img, text_pos)


while True:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if tool == FILL:
                flood_fill(canvas, event.pos, color)

            elif tool == TEXT:
                text_mode = True
                text_pos = event.pos
                text_value = ""

            else:
                drawing = True
                start_pos = event.pos
                last_pos = event.pos

        if event.type == pygame.MOUSEMOTION:
            if drawing:
                if tool == PENCIL:
                    draw_pencil(canvas, color, last_pos, event.pos, size)
                    last_pos = event.pos

                elif tool == ERASER:
                    draw_pencil(canvas, WHITE, last_pos, event.pos, size)
                    last_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                if tool not in [PENCIL, ERASER]:
                    draw_final_shape(event.pos)

            drawing = False
            start_pos = None
            last_pos = None

        if event.type == pygame.KEYDOWN:

#save ctrl+s
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_canvas()

#text typing
            elif text_mode:
                if event.key == pygame.K_RETURN:
                    font = pygame.font.SysFont(None, font_size)
                    img = font.render(text_value, True, color)
                    canvas.blit(img, text_pos)
                    text_mode = False
                    text_value = ""

                elif event.key == pygame.K_ESCAPE:
                    text_mode = False
                    text_value = ""

                elif event.key == pygame.K_BACKSPACE:
                    text_value = text_value[:-1]

                else:
                    text_value += event.unicode

#tools
            elif event.key == pygame.K_p:
                tool = PENCIL
            elif event.key == pygame.K_l:
                tool = LINE
            elif event.key == pygame.K_r:
                tool = RECT
            elif event.key == pygame.K_c:
                tool = CIRCLE
            elif event.key == pygame.K_s:
                tool = SQUARE
            elif event.key == pygame.K_t:
                tool = TEXT
            elif event.key == pygame.K_f:
                tool = FILL
            elif event.key == pygame.K_e:
                tool = ERASER
            elif event.key == pygame.K_1:
                size = 2
            elif event.key == pygame.K_2:
                size = 5
            elif event.key == pygame.K_3:
                size = 10
            elif event.key == pygame.K_4:
                tool = RIGHT_TRIANGLE
            elif event.key == pygame.K_5:
                tool = EQUILATERAL_TRIANGLE
            elif event.key == pygame.K_6:
                tool = RHOMBUS

#colors
            elif event.key == pygame.K_b:
                color = BLACK
            elif event.key == pygame.K_q:
                color = RED
            elif event.key == pygame.K_g:
                color = GREEN
            elif event.key == pygame.K_o:
                color = BLUE
            elif event.key == pygame.K_h:
                color = PINK

#clear
            elif event.key == pygame.K_x:
                canvas.fill(WHITE)

#text size
            elif event.key == pygame.K_LEFTBRACKET:
                font_size = max(15, font_size - 5)
            elif event.key == pygame.K_RIGHTBRACKET:
                font_size += 5

    screen.blit(canvas, (0, 0))

#live preview
    if drawing and tool not in [PENCIL, ERASER]:
        preview = canvas.copy()
        draw_preview(preview, mouse_pos)
        screen.blit(preview, (0, 0))

    draw_text_preview()

    pygame.display.flip()
    clock.tick(120)