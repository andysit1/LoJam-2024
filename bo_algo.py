import pygame
import sys
import math

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Fill Rectangle with Multiple Shapes")

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)




# make grid


# randomize merge the grid




# Rectangle settings
rect_x, rect_y, rect_width, rect_height = 100, 100, 400, 200
shape_spacing = 40  # Spacing between shapes within the rectangle

def draw_triangle(surface, color, center, size):
    """Draws an equilateral triangle centered at `center` with a given `size`."""
    half_size = size // 2
    points = [
        (center[0], center[1] - half_size),  # Top point
        (center[0] - half_size, center[1] + half_size),  # Bottom-left
        (center[0] + half_size, center[1] + half_size)   # Bottom-right
    ]
    pygame.draw.polygon(surface, color, points)

# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Draw the rectangle (optional, to show the boundary)
    pygame.draw.rect(screen, BLUE, (rect_x, rect_y, rect_width, rect_height), 2)

    # Fill the rectangle with alternating shapes
    for i, x in enumerate(range(rect_x + shape_spacing, rect_x + rect_width, shape_spacing)):
        for j, y in enumerate(range(rect_y + shape_spacing, rect_y + rect_height, shape_spacing)):
            position = (x, y)
            pygame.draw.rect(screen, GREEN, (x - shape_spacing // 4, y - shape_spacing // 4, shape_spacing // 2, shape_spacing // 2))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
