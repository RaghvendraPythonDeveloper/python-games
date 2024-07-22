import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced Pygame Game")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Square (player) properties
square_size = 50
square_x, square_y = WIDTH // 2, HEIGHT - square_size - 10
speed = 5

# Bullet properties
bullet_size = 10
bullet_speed = 7
bullets = []

# Falling block properties
block_size = 50
falling_blocks = []
fall_speed = 5
spawn_interval = 25  # Frames between spawns
spawn_timer = 0

# Game state
blocks_destroyed = 0
start_time = time.time()

def spawn_falling_block():
    x = random.randint(0, WIDTH - block_size)
    return pygame.Rect(x, -block_size, block_size, block_size)

def draw_status_bar():
    # Draw status bar background
    pygame.draw.rect(screen, BLACK, pygame.Rect(0, 0, WIDTH, 40))
    
    # Draw text
    font = pygame.font.SysFont(None, 30)
    
    # Calculate time spent
    elapsed_time = int(time.time() - start_time)
    time_text = f"Time: {elapsed_time // 60}:{elapsed_time % 60:02d}"
    
    # Create the text surface and blit it
    time_surface = font.render(time_text, True, WHITE)
    screen.blit(time_surface, (10, 10))
    
    # Draw blocks destroyed
    blocks_text = f"Blocks Destroyed: {blocks_destroyed}"
    blocks_surface = font.render(blocks_text, True, WHITE)
    screen.blit(blocks_surface, (WIDTH - 200, 10))

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Create a new bullet
                bullet_rect = pygame.Rect(square_x + square_size // 2 - bullet_size // 2, square_y - bullet_size, bullet_size, bullet_size)
                bullets.append(bullet_rect)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        square_x -= speed
    if keys[pygame.K_RIGHT]:
        square_x += speed

    # Prevent the player square from going off-screen
    square_x = max(0, min(WIDTH - square_size, square_x))

    # Update bullet positions
    bullets = [bullet.move(0, -bullet_speed) for bullet in bullets if bullet.bottom > 40]  # Keep bullets within the game area

    # Update falling blocks
    falling_blocks = [block.move(0, fall_speed) for block in falling_blocks if block.top < HEIGHT]

    # Check for collisions
    for bullet in bullets:
        for block in falling_blocks:
            if bullet.colliderect(block):
                falling_blocks.remove(block)
                bullets.remove(bullet)
                blocks_destroyed += 1
                break

    for block in falling_blocks:
        if block.colliderect(pygame.Rect(square_x, square_y, square_size, square_size)):
            print("You die!")
            pygame.quit()
            sys.exit()

    # Spawn new falling blocks
    spawn_timer += 1
    if spawn_timer >= spawn_interval:
        falling_blocks.append(spawn_falling_block())
        spawn_timer = 0

    # Clear the screen
    screen.fill(WHITE)
    
    # Draw the status bar
    draw_status_bar()

    # Draw the player square
    pygame.draw.rect(screen, RED, pygame.Rect(square_x, square_y, square_size, square_size))

    # Draw the bullets
    for bullet in bullets:
        pygame.draw.rect(screen, BLUE, bullet)

    # Draw the falling blocks
    for block in falling_blocks:
        pygame.draw.rect(screen, GREEN, block)

    # Update the display
    pygame.display.flip()

    # Add a delay to control frame rate
    pygame.time.delay(30)
