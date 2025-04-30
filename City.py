import pygame
import random
from noise import pnoise2

# Initialize pygame
pygame.init()

# Settings
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 40  # Grid cell size
ROAD_WIDTH = 6  # Width of roads
BUILDING_SIZE = (20, 40)  # Minimum/Maximum building size (width, height)
SEED = random.randint(0, 100)

# Colors
WHITE = (255, 255, 255)
BLACK = (10, 10, 20)
ROAD_COLOR = (100, 100, 100)
BUILDING_COLOR = (200, 200, 255)
PARK_COLOR = (50, 200, 50)

# Initialize screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Procedural City Generator")
clock = pygame.time.Clock()

# Function to generate buildings and parks
def generate_building(x, y):
    # Generate a random building size and color
    width = random.randint(*BUILDING_SIZE)
    height = random.randint(30, 100)
    return pygame.Rect(x, y, width, height)

def generate_city():
    city_grid = []
    for y in range(0, HEIGHT, GRID_SIZE):
        for x in range(0, WIDTH, GRID_SIZE):
            # Decide if the current grid square is a road, building, or park
            if x % (GRID_SIZE * 3) == 0 or y % (GRID_SIZE * 3) == 0:  # Road placement
                city_grid.append(('road', pygame.Rect(x, y, ROAD_WIDTH, GRID_SIZE)))
            else:
                # Use Perlin noise to decide if it's a building or park
                nx = x / WIDTH
                ny = y / HEIGHT
                noise_val = (pnoise2(nx + SEED, ny + SEED) + 0.5)  # Normalize noise to [0, 1]

                # Buildings in higher density areas (more noise = more buildings)
                if noise_val > 0.3:
                    city_grid.append(('building', generate_building(x, y)))
                elif noise_val > 0.1:
                    city_grid.append(('park', pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)))
    return city_grid

# Generate the city layout
city = generate_city()

# Main game loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the city elements
    for element_type, rect in city:
        if element_type == 'road':
            pygame.draw.rect(screen, ROAD_COLOR, rect)
        elif element_type == 'building':
            pygame.draw.rect(screen, BUILDING_COLOR, rect)
        elif element_type == 'park':
            pygame.draw.rect(screen, PARK_COLOR, rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
