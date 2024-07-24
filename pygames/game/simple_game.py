import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)  # Allow resizing
pygame.display.set_caption("Space Adventure")

# Load space background image
space_background = pygame.image.load('D:\pygames\spaceArt\png\Background\starBackground.png')
space_background = pygame.transform.scale(space_background, (WIDTH, HEIGHT))

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Player (spaceship) properties
player_img = pygame.image.load('D:\pygames\spaceArt\png\player.png')  # Load your spaceship image
player_img = pygame.transform.scale(player_img, (50, 50))
player_x, player_y = WIDTH // 2, HEIGHT - 60
speed = 5

# Bullet properties
bullet_img = pygame.image.load('D:\pygames\spaceArt\png\laserGreen.png')  # Load your bullet image (e.g., laser)
bullet_img = pygame.transform.scale(bullet_img, (10, 20))
bullet_speed = 7
bullets = []
bullet_cooldown = 250  # Cooldown time in milliseconds
last_shot_time = 0

# Falling block (asteroid) properties
asteroid_img = pygame.image.load('D:\pygames\spaceArt\png\meteorBig.png')  # Load your asteroid image
asteroid_img = pygame.transform.scale(asteroid_img, (50, 50))
falling_blocks = []
fall_speed = 5
spawn_interval = 25  # Frames between spawns
spawn_timer = 0

# Difficult box properties
difficult_img = pygame.image.load('D:\pygames\spaceArt\png\meteorBig.png')  # Load your difficult box image
difficult_img = pygame.transform.scale(difficult_img, (60, 60))
difficult_boxes = []
difficult_spawn_timer = 0
difficult_spawn_interval = 300  # Spawn every 10 seconds
difficult_health = 4

# Boss properties
boss_img = pygame.image.load('D:\pygames\spaceArt\png\enemyUFO.png')  # Load your boss image
boss_img = pygame.transform.scale(boss_img, (100, 100))
boss = None
boss_health = 20
boss_bullet_img = pygame.image.load('D:\pygames\spaceArt\png\laserRed.png')  # Load your boss bullet image
boss_bullet_img = pygame.transform.scale(boss_bullet_img, (10, 20))
boss_bullets = []
boss_bullet_speed = 4
boss_shoot_interval = 1000  # Shoot every second
boss_last_shot_time = 0
boss_direction = 1
boss_speed = 3

# Game state
blocks_destroyed = 0
start_time = 0
game_active = False  # Flag to check if the game is active

def spawn_falling_block():
    x = random.randint(0, WIDTH - 50)
    return pygame.Rect(x, -50, 50, 50)

def spawn_difficult_box():
    x = random.randint(0, WIDTH - 60)
    return pygame.Rect(x, -60, 60, 60), difficult_health

def draw_status_bar():
    # Draw status bar background
    pygame.draw.rect(screen, (0, 0, 0, 128), pygame.Rect(0, 0, WIDTH, 40))  # Semi-transparent bar

    # Draw text
    font = pygame.font.SysFont(None, 30)

    # Calculate time spent
    elapsed_time = int(time.time() - start_time)
    time_text = f"Time: {elapsed_time // 60}:{elapsed_time % 60:02d}"

    # Create the text surface and blit it
    time_surface = font.render(time_text, True, WHITE)
    screen.blit(time_surface, (10, 10))

    # Draw blocks destroyed
    blocks_text = f"Asteroids Destroyed: {blocks_destroyed}"
    blocks_surface = font.render(blocks_text, True, WHITE)
    screen.blit(blocks_surface, (WIDTH - 220, 10))

def draw_start_screen():
    screen.blit(space_background, (0, 0))  # Draw the space background

    font = pygame.font.SysFont(None, 74)
    title_surface = font.render("Space Adventure", True, WHITE)
    screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, HEIGHT // 2 - 100))

    font_small = pygame.font.SysFont(None, 36)
    start_surface = font_small.render("Press ENTER to Start", True, GREEN)
    quit_surface = font_small.render("Press ESC to Quit", True, RED)

    screen.blit(start_surface, (WIDTH // 2 - start_surface.get_width() // 2, HEIGHT // 2))
    screen.blit(quit_surface, (WIDTH // 2 - quit_surface.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()

# Main game loop
while True:
    if not game_active:
        # Show the start screen
        draw_start_screen()

        # Check for start or quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Start game on Enter key
                    game_active = True
                    blocks_destroyed = 0
                    falling_blocks = []
                    bullets = []
                    boss_bullets = []
                    difficult_boxes = []
                    boss = None
                    start_time = time.time()
                elif event.key == pygame.K_ESCAPE:  # Quit on Escape key
                    pygame.quit()
                    sys.exit()

    else:
        # Game is active, handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Return to start screen on Escape key
                    game_active = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= speed
        if keys[pygame.K_RIGHT]:
            player_x += speed
        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - last_shot_time >= bullet_cooldown:
                # Create a new bullet
                bullet_rect = pygame.Rect(player_x + 20, player_y, 10, 20)
                bullets.append(bullet_rect)
                last_shot_time = current_time

        # Prevent the player from going off-screen
        player_x = max(0, min(WIDTH - 50, player_x))

        # Update bullet positions
        bullets = [bullet.move(0, -bullet_speed) for bullet in bullets if bullet.bottom > 40]  # Keep bullets within the game area

        # Update falling blocks
        falling_blocks = [block.move(0, fall_speed) for block in falling_blocks if block.top < HEIGHT]

        # Update difficult boxes
        for box, health in difficult_boxes:
            box.move_ip(0, fall_speed)

        # Spawn new falling blocks
        spawn_timer += 1
        if spawn_timer >= spawn_interval:
            falling_blocks.append(spawn_falling_block())
            spawn_timer = 0

        # Spawn difficult boxes
        difficult_spawn_timer += 1
        if difficult_spawn_timer >= difficult_spawn_interval:
            difficult_boxes.append(spawn_difficult_box())
            difficult_spawn_timer = 0

        # Handle collisions
        for bullet in bullets:
            for block in falling_blocks:
                if bullet.colliderect(block):
                    falling_blocks.remove(block)
                    bullets.remove(bullet)
                    blocks_destroyed += 1
                    break

            for i, (box, health) in enumerate(difficult_boxes):
                if bullet.colliderect(box):
                    health -= 1
                    bullets.remove(bullet)
                    if health <= 0:
                        difficult_boxes.pop(i)
                        blocks_destroyed += 1
                    else:
                        difficult_boxes[i] = (box, health)
                    break

        # Handle player collision with falling blocks and boxes
        player_rect = pygame.Rect(player_x, player_y, 50, 50)
        for block in falling_blocks:
            if block.colliderect(player_rect):
                print("You die!")
                game_active = False
                break

        for box, health in difficult_boxes:
            if box.colliderect(player_rect):
                print("You die!")
                game_active = False
                break

        # Check if the boss should appear
        if blocks_destroyed >= 20 and boss is None:
            boss = pygame.Rect(WIDTH // 2 - 50, 50, 100, 100)  # Initialize boss position
            boss_last_shot_time = pygame.time.get_ticks()  # Reset shooting timer

        # Update boss and handle boss actions
        if boss:
            # Move boss
            boss.x += boss_speed * boss_direction
            if boss.left < 0 or boss.right > WIDTH:
                boss_direction *= -1  # Change direction if at screen edge

            # Boss shooting logic
            current_time = pygame.time.get_ticks()
            if current_time - boss_last_shot_time >= boss_shoot_interval:
                # Create a boss bullet
                boss_bullet_rect = pygame.Rect(boss.centerx - 5, boss.bottom, 10, 20)
                boss_bullets.append(boss_bullet_rect)
                boss_last_shot_time = current_time

            # Update boss bullet positions
            boss_bullets = [bullet.move(0, boss_bullet_speed) for bullet in boss_bullets if bullet.top < HEIGHT]

            # Handle player collision with boss bullets
            for bullet in boss_bullets:
                if bullet.colliderect(player_rect):
                    print("You die!")
                    game_active = False
                    break

            # Handle player bullet collision with boss
            for bullet in bullets:
                if bullet.colliderect(boss):
                    boss_health -= 1
                    bullets.remove(bullet)
                    if boss_health <= 0:
                        print("You defeated the boss!")
                        game_active = False
                    break

        # Clear the screen
        screen.blit(space_background, (0, 0))  # Use the space background

        # Draw the status bar
        draw_status_bar()

        # Draw the player (spaceship)
        screen.blit(player_img, (player_x, player_y))

        # Draw the bullets
        for bullet in bullets:
            screen.blit(bullet_img, bullet)

        # Draw the falling blocks (asteroids)
        for block in falling_blocks:
            screen.blit(asteroid_img, block)

        # Draw the difficult boxes
        for box, health in difficult_boxes:
            screen.blit(difficult_img, box)

        # Draw the boss and boss bullets if present
        if boss:
            screen.blit(boss_img, boss)
            for bullet in boss_bullets:
                screen.blit(boss_bullet_img, bullet)

        # Update the display
        pygame.display.flip()

        # Add a delay to control frame rate
        pygame.time.delay(30)
