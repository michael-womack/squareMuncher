import pygame
import random

# Initialize pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Square Muncher")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Set up the player
player_size = 20
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 5

# Set up the food
food_size = 10
food_count = 25  # Increased to 25 smaller squares
foods = []

# Set up the enemies
enemy_size = 20  # Twice the size of the red squares
enemies = []


# Function to initialize food and enemy objects
def reset_game():
    global player_x, player_y, player_size, score, game_over
    player_x = WIDTH // 2
    player_y = HEIGHT // 2
    player_size = 20
    score = 0
    game_over = False
    foods.clear()
    enemies.clear()

    for _ in range(food_count):
        food = {
            "x": random.randint(0, WIDTH - food_size),
            "y": random.randint(0, HEIGHT - food_size),
            "dx": random.choice([-1, 1]) * random.uniform(0.5, 1.5),
            "dy": random.choice([-1, 1]) * random.uniform(0.5, 1.5),
            "size": food_size,
        }
        foods.append(food)

    for _ in range(2):
        enemy = {
            "x": random.randint(0, WIDTH - enemy_size),
            "y": random.randint(0, HEIGHT - enemy_size),
            "dx": random.choice([-1, 1]) * random.uniform(0.5, 1.5),
            "dy": random.choice([-1, 1]) * random.uniform(0.5, 1.5),
            "size": enemy_size,
        }
        enemies.append(enemy)


# Initialize game objects
reset_game()

# Font setup
font = pygame.font.Font(None, 36)

# Game loop variables
running = True
game_over = False
clock = pygame.time.Clock()
in_title_screen = True  # Flag for the title screen


# Function to move objects (food and enemies)
def move_object(obj, speed_factor=1):
    obj["x"] += obj["dx"] * speed_factor
    obj["y"] += obj["dy"] * speed_factor

    if obj["x"] <= 0 or obj["x"] >= WIDTH - obj["size"]:
        obj["dx"] *= -1
    if obj["y"] <= 0 or obj["y"] >= HEIGHT - obj["size"]:
        obj["dy"] *= -1

    obj["x"] = max(0, min(WIDTH - obj["size"], obj["x"]))
    obj["y"] = max(0, min(HEIGHT - obj["size"], obj["y"]))


# Function to check for collisions
def check_collision(player_x, player_y, player_size, obj_x, obj_y, obj_size):
    return (player_x < obj_x + obj_size and player_x + player_size > obj_x and
            player_y < obj_y + obj_size and player_y + player_size > obj_y)


# Title screen display function
def display_title_screen():
    title_font = pygame.font.Font(None, 108)
    title_text = title_font.render("Square Muncher", True, GREEN)
    instruction_text = font.render("Eat the RED squares,", True, RED)
    instruction_text2 = font.render("Avoid the BLUE ones!", True, BLUE)
    press_enter_text = font.render("Press ENTER to begin", True, YELLOW)
    screen.fill(BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))

    # First instruction line
    screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 - 20))
    # Second instruction line, slightly below the first
    screen.blit(instruction_text2, (WIDTH // 2 - instruction_text2.get_width() // 2, HEIGHT // 2 + 20))
    screen.blit(press_enter_text, (WIDTH // 2 - press_enter_text.get_width() // 2, HEIGHT // 1.5))

    pygame.display.update()


# Main game loop
while running:
    if in_title_screen:
        display_title_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    in_title_screen = False
                    reset_game()

        continue  # Skip the rest of the loop if we're on the title screen

    screen.fill(BLACK)

    if game_over:
        # Display GAME OVER screen
        game_over_text = font.render("GAME OVER", True, WHITE)
        score_text = font.render(f"Score: {score}", True, WHITE)
        restart_text = font.render("Press ENTER to restart", True, YELLOW)

        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 10))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    reset_game()

        continue  # Skip the rest of the loop after game over

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # Restrict player movement within the window
    player_x = max(0, min(WIDTH - player_size, player_x))
    player_y = max(0, min(HEIGHT - player_size, player_y))

    # Check collision with food
    for food in foods:
        if check_collision(player_x, player_y, player_size, food["x"], food["y"], food_size):
            score += 100
            food["x"] = random.randint(0, WIDTH - food_size)
            food["y"] = random.randint(0, HEIGHT - food_size)

    # Check collision with enemies
    for enemy in enemies:
        if check_collision(player_x, player_y, player_size, enemy["x"], enemy["y"], enemy_size):
            game_over = True

    # Move food and enemies
    for food in foods:
        move_object(food)
    for enemy in enemies:
        move_object(enemy, speed_factor=2)

    # Draw player
    pygame.draw.rect(screen, GREEN, (player_x, player_y, player_size, player_size))

    # Draw food
    for food in foods:
        pygame.draw.rect(screen, RED, (food["x"], food["y"], food_size, food_size))

    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(screen, BLUE, (enemy["x"], enemy["y"], enemy_size, enemy_size))

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
