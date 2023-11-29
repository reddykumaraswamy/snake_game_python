import pygame
import pygame.mixer
import random

# Initialize Pygame
pygame.init()

# Setting up the game window
width, height = 720, 480
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gobble Snake Game")

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
grey = (140, 140, 140)
darkGreen = (11, 102, 35)

# Load the background image
background_image = pygame.image.load("images/snake_background.jpg")
# Scale the image to fit the window size
background_image = pygame.transform.scale(background_image, (width, height))

# Load the background image
game_background = pygame.image.load("images/game_bg.png")
# Scale the image to fit the window size
game_background = pygame.transform.scale(game_background, (width, height))

# Define the snake and food sizes
snake_size = 20
food_size = 20
# food_radius = 10

# Initialize the clock to control the frame rate
clock = pygame.time.Clock()

# Define the font for displaying the text
font = pygame.font.SysFont('Bookman Old Style', 22, 'bold')

# Initialize the mixer
pygame.mixer.init()

# Load and play the background music
pygame.mixer.music.load("audio/Snake Game - Theme Song.mp3")
# pygame.mixer.music.load("audio/Kgf Eagle - sound.mp3")
pygame.mixer.music.play(-1)  # -1 means loop indefinitely
pygame.mixer.music.set_volume(0.5)  # Adjusting the volume

# Loading the eat sound effect
eat_sound = pygame.mixer.Sound("audio/reward_sound.mp3")
# Loading the collide sound effect
collide_sound = pygame.mixer.Sound("audio/hit_sound.mp3")


# Function to display text on the screen
def display_text(text, color, x, y):
    rendered_text = font.render(text, True, color)
    window.blit(rendered_text, [x, y])


# Function to display text on the screen with customizable font and size
def display_upper_text(text, color, x, y):
    font = pygame.font.SysFont('Ink Free', 70, 'bold')
    rendered_text = font.render(text, True, color)
    window.blit(rendered_text, [x, y])


# Function to draw the snake
def draw_snake(snake):
    for i, segment in enumerate(snake):
        x, y = segment
        x += (food_size - snake_size) // 2  # Center the segment within the cell
        y += (food_size - snake_size) // 2  # Center the segment within the cell

        if i == 0:  # Tail of the snake
            # pygame.draw.rect(window, white, [x, y, snake_size, snake_size])
            pygame.draw.circle(window, white, (x + snake_size // 2, y + snake_size // 2), snake_size // 2)
        elif i == len(snake) - 1:  # Head of the snake
            # pygame.draw.rect(window, white, [x, y, snake_size, snake_size])
            pygame.draw.circle(window, black, (x + snake_size // 2, y + snake_size // 2), snake_size // 2)

            # Draw eyes as black circles on the head
            eye_radius = 2.6
            # eye_offset = snake_size // 6
            eye_1 = (x + snake_size // 3, y + snake_size // 3)
            eye_2 = (x + snake_size * 2.5 // 3, y + snake_size // 3)
            pygame.draw.circle(window, grey, eye_1, eye_radius)
            pygame.draw.circle(window, grey, eye_2, eye_radius)

        else:  # Body of the snake
            # pygame.draw.rect(window, white, [x, y, snake_size, snake_size])
            pygame.draw.circle(window, white, (x + snake_size // 2, y + snake_size // 2), snake_size // 2)


# Function to generate food at a random position
def generate_food():
    food_x = round(random.randrange(0, width - food_size) / food_size) * food_size
    food_y = round(random.randrange(0, height - food_size) / food_size) * food_size
    return food_x, food_y


# def generate_food():
#     food_x = round(random.randrange(0, width - food_radius * 2) / snake_size) * snake_size
#     food_y = round(random.randrange(0, height - food_radius * 2) / snake_size) * snake_size
#     return food_x, food_y


# Function to display game over message
def game_over(score, player_name):
    window.blit(background_image, (0, 0))
    display_upper_text("GAME OVER", darkGreen, width / 20, height / 6)
    display_text("Player Name: " + player_name, white, width / 10, height / 2.2)
    display_text("Score: " + str(score), white, width / 10, height / 1.8)
    display_text("Press ENTER to play again!", darkGreen, width / 10, height / 1.3)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game()


# Function to create an animated sprite for "Level Up" text
class LevelUpText(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.font = pygame.font.SysFont('Ink Free', 26, 'bold')
        self.image = self.font.render("Speed x2", True, darkGreen)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.animation_count = 0
        self.animation_frames = 30

    def update(self):
        self.animation_count += 1
        if self.animation_count > self.animation_frames:
            self.kill()
        else:
            alpha = int((1 - self.animation_count / self.animation_frames) * 255)
            self.image.set_alpha(alpha)


# Function to run the game
def game():
    # Get player name
    player_name = ""
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode

        window.blit(background_image, (0, 0))
        display_upper_text("Gobble Snake", darkGreen, width / 18, height / 8)
        display_text("Enter Your Name:", white, width / 8, height / 3)
        pygame.draw.rect(window, white, [width / 8, height / 2.4, width / 3, 30])
        display_text(player_name, black, width / 8 + 5, height / 2.42 + 5)
        pygame.display.update()

    # Initialize the snake and food positions
    snake_x = width / 2
    snake_y = height / 2
    snake_dx = snake_size
    snake_dy = 0
    snake = []
    snake_length = 3

    food_x, food_y = generate_food()

    score = 0

    # Game speed variables
    level_threshold = 10  # Score threshold to advance to the next level
    clock_tick_rate = 10  # Initial speed of the game

    game_over_flag = False
    game_exit = False

    # Create a sprite group for level up text
    level_up_texts = pygame.sprite.Group()

    while not game_exit:
        while game_over_flag:
            game_over(score, player_name)
            game_exit = True
            game_over_flag = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    snake_dx = -snake_size
                    snake_dy = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    snake_dx = snake_size
                    snake_dy = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    snake_dy = -snake_size
                    snake_dx = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    snake_dy = snake_size
                    snake_dx = 0

        if snake_x >= width or snake_x < 0 or snake_y >= height or snake_y < 0:
            collide_sound.play()
            pygame.time.delay(1000)
            game_over_flag = True

        snake_x += snake_dx
        snake_y += snake_dy

        # if snake_x >= width:
        #     snake_x = 0
        # elif snake_x < 0:
        #     snake_x = width - snake_size
        # if snake_y >= height:
        #     snake_y = 0
        # elif snake_y < 0:
        #     snake_y = height - snake_size

        window.blit(game_background, (0, 0))
        pygame.draw.rect(window, red, [food_x, food_y, food_size, food_size])
        # pygame.draw.circle(window, red, (food_x + food_radius, food_y + food_radius), food_radius)
        snake_head = [snake_x, snake_y]
        # snake_head.append(snake_x)
        # snake_head.append(snake_y)
        snake.append(snake_head)

        if len(snake) > snake_length:
            del snake[0]

        for segment in snake[:-1]:
            if segment == snake_head:
                collide_sound.play()
                pygame.time.delay(1000)
                game_over_flag = True

        draw_snake(snake)
        display_text("Your Score: " + str(score), black, 10, 10)

        # Update and draw the level up texts
        level_up_texts.update()
        level_up_texts.draw(window)

        pygame.display.update()

        if snake_head[0] == food_x and snake_head[1] == food_y:
            food_x, food_y = generate_food()
            snake_length += 1
            score += 5
            eat_sound.play()

            # Create and add a level up text sprite
            level_up_text = LevelUpText(width / 2, height / 2)
            level_up_texts.add(level_up_text)

        # clock.tick(10)  # Adjust the speed of the game

        # Inside the game loop, where the score is updated
        if score >= level_threshold:
            level_threshold += 10
            clock_tick_rate += 1

        clock.tick(clock_tick_rate)

    pygame.quit()
    quit()


# Run the game
game()
