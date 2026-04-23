import pygame
import os

class MusicPlayer:
    def __init__(self, screen):
        self.screen = screen

        # Define font for displaying text
        self.font = pygame.font.SysFont("Arial", 28, bold=True)

        # Paths to the music tracks
        self.tracks = [
            os.path.join("music", "track1.wav"),
            os.path.join("music", "track2.wav"),
        ]
        self.index = 0  # Keeps track of the current track
        self.is_playing = False  # Flag to check if music is playing

        # Initialize pygame mixer for audio playback
        pygame.mixer.init()

    def load_current(self):
        """Load the current track for playback"""
        pygame.mixer.music.load(self.tracks[self.index])

    def play(self):
        """Play the current track"""
        self.load_current()
        pygame.mixer.music.play()  # Play the track
        self.is_playing = True

    def stop(self):
        """Stop the current music"""
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        """Play the next track in the list"""
        self.index = (self.index + 1) % len(self.tracks)  # Loop back to the first track
        self.play()

    def previous_track(self):
        """Play the previous track in the list"""
        self.index = (self.index - 1) % len(self.tracks)  # Loop to the last track
        self.play()

    def draw(self):
        """Draw the player interface on the screen"""
        self.screen.fill((240, 240, 240))  # Fill the screen with a light color

        # Set the color for the text (pink)
        text_color = (255, 105, 180)

        # Render the title, current track, and controls text
        title = self.font.render("Music Player", True, text_color)
        current = self.font.render(f"Track: {os.path.basename(self.tracks[self.index])}", True, text_color)
        controls = self.font.render("P=Play  S=Stop  N=Next  B=Back  Q=Quit", True, text_color)

        # Get the current position of the music (in seconds)
        pos_ms = pygame.mixer.music.get_pos()
        seconds = max(0, pos_ms // 1000)  # Position in seconds
        progress = self.font.render(f"Position: {seconds} sec", True, text_color)

        # Center the text elements on the screen
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 100))
        current_rect = current.get_rect(center=(self.screen.get_width() // 2, 200))
        progress_rect = progress.get_rect(center=(self.screen.get_width() // 2, 300))
        controls_rect = controls.get_rect(center=(self.screen.get_width() // 2, 400))

        # Blit (draw) the texts onto the screen
        self.screen.blit(title, title_rect)
        self.screen.blit(current, current_rect)
        self.screen.blit(progress, progress_rect)
        self.screen.blit(controls, controls_rect)