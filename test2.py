import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Randomized Shapes in Rectangle")

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Rectangle settings
rect_x, rect_y, rect_width, rect_height = 100, 100, 400, 200
shape_count = 100  # Number of shapes to generate

def draw_triangle(surface, color, center, size, angle=0):
    """Draws a triangle centered at `center` with a given `size` and `angle`."""
    half_size = size // 2
    angle_rad = math.radians(angle)
    points = [
        (center[0] + half_size * math.cos(angle_rad),
         center[1] - half_size * math.sin(angle_rad)),
        (center[0] - half_size * math.cos(angle_rad + math.pi / 3),
         center[1] + half_size * math.sin(angle_rad + math.pi / 3)),
        (center[0] - half_size * math.cos(angle_rad - math.pi / 3),
         center[1] + half_size * math.sin(angle_rad - math.pi / 3)),
    ]
    pygame.draw.polygon(surface, color, points)

# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Draw the rectangle boundary (optional)
    pygame.draw.rect(screen, BLUE, (rect_x, rect_y, rect_width, rect_height), 2)

    # Generate random shapes within the rectangle
    for _ in range(shape_count):
        # Random position within the rectangle
        x = random.randint(rect_x, rect_x + rect_width)
        y = random.randint(rect_y, rect_y + rect_height)
        position = (x, y)

        # Random size and angle
        size = random.randint(10, 20)
        angle = random.randint(0, 360)

        # Randomly select a shape type
        shape_type = random.choice(['circle', 'square', 'triangle'])

        # Draw the shape
        if shape_type == 'circle':
            pygame.draw.circle(screen, RED, position, size)
        elif shape_type == 'square':
            pygame.draw.rect(
                screen,
                GREEN,
                (x - size // 2, y - size // 2, size, size),
                border_radius=random.randint(0, size // 2)
            )
        elif shape_type == 'triangle':
            draw_triangle(screen, BLUE, position, size, angle)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
