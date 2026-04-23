import pygame
from clock import MickeyClock, WIDTH, HEIGHT

pygame.init()

# Set the screen size (900x700 pixels)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")  # Window title

# Set up the clock and the MickeyClock app
clock = pygame.time.Clock()
app = MickeyClock(screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the user closes the window, stop the loop
            running = False

    app.draw()  # Draw the clock on the screen
    pygame.display.flip()  # Update the screen with the new drawing

    clock.tick(1)  # Run the clock at 1 frame per second (update every second)

pygame.quit()