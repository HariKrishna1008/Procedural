import pygame
import random

# Map settings
TILE_SIZE = 20
MAP_WIDTH = 40
MAP_HEIGHT = 20
SCREEN_WIDTH = MAP_WIDTH * TILE_SIZE
SCREEN_HEIGHT = MAP_HEIGHT * TILE_SIZE

# Dungeon settings
NUM_ROOMS = 5
ROOM_MIN_SIZE = 3
ROOM_MAX_SIZE = 6

# Colors
WALL_COLOR = (30, 30, 30)
FLOOR_COLOR = (200, 200, 200)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Procedural Dungeon")

# Create dungeon map
dungeon = [['#' for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]

def create_room(x, y, w, h):
    for i in range(y, y + h):
        for j in range(x, x + w):
            if 0 <= i < MAP_HEIGHT and 0 <= j < MAP_WIDTH:
                dungeon[i][j] = '.'

def connect_rooms(x1, y1, x2, y2):
    if random.random() < 0.5:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            dungeon[y1][x] = '.'
        for y in range(min(y1, y2), max(y1, y2) + 1):
            dungeon[y][x2] = '.'
    else:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            dungeon[y][x1] = '.'
        for x in range(min(x1, x2), max(x1, x2) + 1):
            dungeon[y2][x] = '.'

# Generate rooms and corridors
rooms = []
for _ in range(NUM_ROOMS):
    w = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
    h = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
    x = random.randint(1, MAP_WIDTH - w - 1)
    y = random.randint(1, MAP_HEIGHT - h - 1)

    create_room(x, y, w, h)
    if rooms:
        prev_x, prev_y = rooms[-1]
        connect_rooms(prev_x, prev_y, x + w // 2, y + h // 2)
    rooms.append((x + w // 2, y + h // 2))

# Game loop
running = True
while running:
    screen.fill(WALL_COLOR)

    # Draw dungeon
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if dungeon[y][x] == '.':
                pygame.draw.rect(screen, FLOOR_COLOR, (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
