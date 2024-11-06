import pygame
import random
import sys

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Random Rectangles in Rectangle")

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Main rectangle bounds
rect_x, rect_y, rect_width, rect_height = 100, 100, 400, 200
rect_area = pygame.Rect(rect_x, rect_y, rect_width, rect_height)

# Parameters
min_size = 10   # Minimum size of random rectangles
max_size = 50   # Maximum size of random rectangles
rectangle_count = 20  # Number of rectangles to try to place
attempt_limit = 1000  # Limit of attempts to place rectangles

# Function to generate a random rectangle within bounds
def generate_random_rectangle(area):
    width = random.randint(min_size, max_size)
    height = random.randint(min_size, max_size)
    x = random.randint(area.left, area.right - width)
    y = random.randint(area.top, area.bottom - height)
    return pygame.Rect(x, y, width, height)

# Place rectangles
rectangles = []
attempts = 0

while len(rectangles) < rectangle_count and attempts < attempt_limit:
    # Generate a random rectangle
    new_rect = generate_random_rectangle(rect_area)
    # Check for overlap with existing rectangles
    if all(not new_rect.colliderect(r) for r in rectangles):
        rectangles.append(new_rect)  # Add to list if no overlap
    else:
        # Reduce size if collision occurs and retry
        new_rect.width = max(new_rect.width - 5, min_size)
        new_rect.height = max(new_rect.height - 5, min_size)
    attempts += 1

# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Draw main rectangle outline
    pygame.draw.rect(screen, BLUE, rect_area, 2)

    # Draw all successfully placed rectangles
    for rect in rectangles:
        pygame.draw.rect(screen, GREEN, rect)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
