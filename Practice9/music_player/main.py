import pygame
from player import MusicPlayer

def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((800, 500))
    pygame.display.set_caption("Music Player")
    clock = pygame.time.Clock()

    player = MusicPlayer(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    player.play()
                elif event.key == pygame.K_s:
                    player.stop()
                elif event.key == pygame.K_n:
                    player.next_track()
                elif event.key == pygame.K_b:
                    player.previous_track()
                elif event.key == pygame.K_q:
                    running = False

        player.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.mixer.music.stop()
    pygame.quit()

if __name__ == "__main__":
    main()