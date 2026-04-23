import pygame
import datetime
import os

WIDTH, HEIGHT = 900, 700

# The center of the window
WINDOW_CENTER = (WIDTH // 2, HEIGHT // 2)

# The center of the clock (the pivot point for the hands)
CLOCK_CENTER = pygame.math.Vector2(450, 360)

class MickeyClock:
    def __init__(self, screen):
        self.screen = screen

        # Paths to the images for left and right hands and the clock background
        left_path = os.path.join("images", "mickey_left_hand.png")
        right_path = os.path.join("images", "mickey_right_hand.png")
        bg_path = os.path.join("images", "clock_bg.png")

        # Load the hand images and clock background
        self.left_hand = pygame.image.load(left_path).convert_alpha()
        self.right_hand = pygame.image.load(right_path).convert_alpha()
        self.bg = pygame.image.load(bg_path).convert_alpha()

        # Resize the clock background to fit the window size
        self.bg = pygame.transform.scale(self.bg, (850, 850))
        self.bg_rect = self.bg.get_rect(center=WINDOW_CENTER)

        # Resize the hands to a reasonable size
        self.left_hand = pygame.transform.scale(self.left_hand, (260, 260))
        self.right_hand = pygame.transform.scale(self.right_hand, (260, 260))

        # Define the rotation pivot points for the hands (the shoulders of Mickey)
        self.left_anchor = pygame.math.Vector2(130, 130)  # Left hand anchor
        self.right_anchor = pygame.math.Vector2(130, 130)  # Right hand anchor

    def blit_rotate(self, image, pivot_screen, anchor_in_image, angle):
        """
        This method rotates an image around a specified pivot point on the screen.
        The image is rotated based on the angle, and the rotation is done around the 'anchor' point of the hand.
        """
        # Get the rectangle of the image with its top-left corner at the pivot point minus the anchor position
        image_rect = image.get_rect(topleft=(pivot_screen.x - anchor_in_image.x,
                                            pivot_screen.y - anchor_in_image.y))

        # Calculate the offset between the image center and the pivot point
        offset_center_to_pivot = pygame.math.Vector2(pivot_screen) - image_rect.center
        rotated_offset = offset_center_to_pivot.rotate(-angle)

        # Calculate the new center for the rotated image
        rotated_center = (pivot_screen.x - rotated_offset.x,
                          pivot_screen.y - rotated_offset.y)

        # Rotate the image
        rotated_image = pygame.transform.rotate(image, angle)

        # Get the rectangle of the rotated image
        rotated_rect = rotated_image.get_rect(center=rotated_center)

        # Blit (draw) the rotated image to the screen
        self.screen.blit(rotated_image, rotated_rect)

    def draw(self):
        """
        This method draws the clock and the hands on the screen.
        It updates the clock face and draws the rotating hands.
        """
        self.screen.fill((255, 255, 255))  # Clear the screen with a white color

        # Draw the clock background centered on the screen
        self.screen.blit(self.bg, self.bg_rect)

        # Get the current time (minutes and seconds)
        now = datetime.datetime.now()
        minutes = now.minute
        seconds = now.second

        # Calculate the angle for the minute and second hands
        minute_angle = -minutes * 6  # Each minute corresponds to a 6 degree rotation
        second_angle = -seconds * 6  # Each second corresponds to a 6 degree rotation

        # Draw the right hand (minute hand)
        self.blit_rotate(self.right_hand, CLOCK_CENTER, self.right_anchor, minute_angle)

        # Draw the left hand (second hand)
        # Slightly shifted to differentiate the two hands visually
        self.blit_rotate(self.left_hand, CLOCK_CENTER, self.left_anchor, second_angle)