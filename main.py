import pygame
import random
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
light_blue = (173, 216, 230)
button_color = (0, 255, 127)
hover_color = (50, 205, 50)
snake_body_color = (34, 139, 34)  # Forest Green

# Screen dimensions
screen_width = 950
screen_height = 500
gamewindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game Final")

# Load Images
snake_size = 30
red_apple_img = pygame.transform.scale(pygame.image.load("red_apple.png"), (snake_size, snake_size))
green_apple_img = pygame.transform.scale(pygame.image.load("green_apple.png"), (snake_size, snake_size))
mango_img = pygame.transform.scale(pygame.image.load("mango.png"), (snake_size, snake_size))
frog_img = pygame.transform.scale(pygame.image.load("frog.png"), (snake_size, snake_size))
food_images = [("Red Apple", red_apple_img), ("Green Apple", green_apple_img), ("Mango", mango_img), ("Frog", frog_img)]

# Load Sounds
pygame.mixer.music.load('background_music.mp3')
eat_sound = pygame.mixer.Sound('eat_sound.wav')

# Fonts & Clock
font = pygame.font.SysFont(None, 55)
clock = pygame.time.Clock()

# High Score File Handling
if not os.path.exists("highscore.txt"):
    with open("highscore.txt", "w") as f:
        f.write("0")
with open("highscore.txt", "r") as f:
    hs = f.read().strip()
    highscore = int(hs) if hs.isdigit() else 0

# Functions
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gamewindow.blit(screen_text, [x, y])

def draw_snake_block(x, y, color):
    pygame.draw.rect(gamewindow, black, [x, y, snake_size, snake_size])  # Border
    pygame.draw.rect(gamewindow, color, [x + 2, y + 2, snake_size - 4, snake_size - 4])

def draw_snake_head(x, y, direction, bite=False):
    pygame.draw.rect(gamewindow, snake_body_color, [x, y, snake_size, snake_size])

    eye_white_radius = 5
    pupil_radius = 2
    shine_radius = 1

    if direction == "RIGHT":
        eye1 = (x + snake_size - 8, y + 8)
        eye2 = (x + snake_size - 8, y + snake_size - 8)
        tongue_start = (x + snake_size, y + snake_size // 2)
        tongue_left = (x + snake_size + 10, y + snake_size // 2 - 3)
        tongue_right = (x + snake_size + 10, y + snake_size // 2 + 3)
        mouth_rect = pygame.Rect(x + snake_size - 5, y + snake_size // 2 - 5, 10, 10)
    elif direction == "LEFT":
        eye1 = (x + 8, y + 8)
        eye2 = (x + 8, y + snake_size - 8)
        tongue_start = (x, y + snake_size // 2)
        tongue_left = (x - 10, y + snake_size // 2 - 3)
        tongue_right = (x - 10, y + snake_size // 2 + 3)
        mouth_rect = pygame.Rect(x - 5, y + snake_size // 2 - 5, 10, 10)
    elif direction == "UP":
        eye1 = (x + 8, y + 8)
        eye2 = (x + snake_size - 8, y + 8)
        tongue_start = (x + snake_size // 2, y)
        tongue_left = (x + snake_size // 2 - 3, y - 10)
        tongue_right = (x + snake_size // 2 + 3, y - 10)
        mouth_rect = pygame.Rect(x + snake_size // 2 - 5, y - 5, 10, 10)
    else:  # DOWN
        eye1 = (x + 8, y + snake_size - 8)
        eye2 = (x + snake_size - 8, y + snake_size - 8)
        tongue_start = (x + snake_size // 2, y + snake_size)
        tongue_left = (x + snake_size // 2 - 3, y + snake_size + 10)
        tongue_right = (x + snake_size // 2 + 3, y + snake_size + 10)
        mouth_rect = pygame.Rect(x + snake_size // 2 - 5, y + snake_size - 5, 10, 10)

    for eye in [eye1, eye2]:
        pygame.draw.circle(gamewindow, white, eye, eye_white_radius)
        pygame.draw.circle(gamewindow, black, eye, pupil_radius)
        pygame.draw.circle(gamewindow, white, (eye[0] - 1, eye[1] - 2), shine_radius)

    pygame.draw.line(gamewindow, red, tongue_start, tongue_left, 2)
    pygame.draw.line(gamewindow, red, tongue_start, tongue_right, 2)

    if bite:
        pygame.draw.ellipse(gamewindow, black, mouth_rect)
        tooth_width = 2
        for i in range(3):
            tooth_x = mouth_rect.centerx + i * tooth_width - 3
            tooth_y = mouth_rect.centery
            pygame.draw.polygon(gamewindow, white, [(tooth_x, tooth_y), (tooth_x + 2, tooth_y + 4), (tooth_x - 2, tooth_y + 4)])

def plot_snake(gamewindow, color, snake_list, snake_size, direction, bite=False):
    for i, (x, y) in enumerate(snake_list):
        if i == len(snake_list) - 1:
            draw_snake_head(x, y, direction, bite)
        else:
            draw_snake_block(x, y, color)

def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gamewindow, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            if action == "play":
                game_loop()
            if action == "quit":
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(gamewindow, ic, (x, y, w, h))

    text_screen(msg, black, x + 20, y + 10)

def main_menu():
    pygame.mixer.music.play(-1)
    while True:
        gamewindow.fill(light_blue)
        text_screen("Welcome to Snake Game", black, 250, 150)
        button("Play", 370, 250, 200, 50, button_color, hover_color, "play")
        button("Quit", 370, 330, 200, 50, button_color, hover_color, "quit")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.update()

def game_loop():
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    init_velocity = 5
    snake_list = []
    snake_length = 1
    food_x = random.randint(20, screen_width - 40)
    food_y = random.randint(20, screen_height - 40)
    food_type, food_img = random.choice(food_images)
    score = 0
    pause = False
    game_over = False
    direction = "RIGHT"
    bite_timer = 0
    global highscore

    while not game_over:
        if not pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                        direction = "RIGHT"
                    elif event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                        direction = "LEFT"
                    elif event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                        direction = "UP"
                    elif event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0
                        direction = "DOWN"
                    elif event.key == pygame.K_p:
                        pause = not pause

            snake_x += velocity_x
            snake_y += velocity_y

            if snake_x < 0 or snake_x > screen_width - snake_size or snake_y < 0 or snake_y > screen_height - snake_size:
                game_over = True

            head = [snake_x, snake_y]
            snake_list.append(head)

            if len(snake_list) > snake_length:
                del snake_list[0]

            if head in snake_list[:-1]:
                game_over = True

            if abs(snake_x - food_x) < snake_size and abs(snake_y - food_y) < snake_size:
                score += 1
                eat_sound.play()
                food_x = random.randint(20, screen_width - 40)
                food_y = random.randint(20, screen_height - 40)
                food_type, food_img = random.choice(food_images)
                snake_length += 5
                bite_timer = 10
                if score > highscore:
                    highscore = score

            gamewindow.fill(light_blue)
            text_screen("Score: " + str(score * 10), red, 5, 5)
            text_screen("High Score: " + str(highscore * 10), black, 650, 5)
            gamewindow.blit(food_img, (food_x, food_y))
            plot_snake(gamewindow, snake_body_color, snake_list, snake_size, direction, bite_timer > 0)

            if pause:
                text_screen("Paused", red, screen_width // 2 - 80, screen_height // 2)

            pygame.display.update()
            clock.tick(30)

            if bite_timer > 0:
                bite_timer -= 1
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pause = not pause

    pygame.mixer.music.stop()
    with open("highscore.txt", "w") as f:
        f.write(str(highscore))

    while True:
        gamewindow.fill(light_blue)
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            text_screen("Game Over! Score: " + str(score * 10), red, 250, 200)
        text_screen("High Score: " + str(highscore * 10), black, 250, 260)
        text_screen("Press Enter to Play Again or Esc to Quit", black, 150, 330)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
        pygame.display.update()

# Start the Game
main_menu()