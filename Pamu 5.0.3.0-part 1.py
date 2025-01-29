import random
import pygame
import json
import time

# Game Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
SNAKE_COLOR_1 = (0, 200, 0)
SNAKE_COLOR_2 = (0, 0, 200)
FOOD_COLOR = (200, 0, 0)
BACKGROUND_COLOR = (40, 40, 40)
GRID_COLOR = (60, 60, 60)
FRAME_RATE = 15

# Initialize Pygame
pygame.init()
pygame.display.set_caption("Snake Game")
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# Load sound effects
eat_sound = pygame.mixer.Sound('eat.wav')
crash_sound = pygame.mixer.Sound('crash.wav')

# Load UI assets
font_path = pygame.font.match_font('arial')
score_font = pygame.font.Font(font_path, 24)
title_font = pygame.font.Font(font_path, 48)
pause_font = pygame.font.Font(font_path, 72)
button_font = pygame.font.Font(font_path, 36)

# Game Variables
snake_positions = [[(WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2)], [(3 * WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2)]]
food_position = None
directions = [(0, 1), (0, 1)]
scores = [0, 0]
high_scores = []
paused = False
game_mode = None
challenge_mode = False
challenge_goal = 0
challenge_time = 0
start_time = 0

def load_high_scores():
    global high_scores
    try:
        with open('high_scores.json', 'r') as f:
            high_scores = json.load(f)
    except FileNotFoundError:
        high_scores = []

def save_high_scores():
    with open('high_scores.json', 'w') as f:
        json.dump(high_scores, f)

def get_random_position():
    x = random.randrange(GRID_SIZE, WINDOW_WIDTH - GRID_SIZE, GRID_SIZE)
    y = random.randrange(GRID_SIZE, WINDOW_HEIGHT - GRID_SIZE, GRID_SIZE)
    return (x, y)

def move_snake(index):
    global snake_positions, directions, food_position, scores
    head_x, head_y = snake_positions[index][0]
    new_head_x = (head_x + directions[index][0] * GRID_SIZE) % WINDOW_WIDTH
    new_head_y = (head_y + directions[index][1] * GRID_SIZE) % WINDOW_HEIGHT
    snake_positions[index].insert(0, (new_head_x, new_head_y))

    if (new_head_x, new_head_y) == food_position:
        food_position = get_random_position()
        scores[index] += 1
        eat_sound.play()
    else:
        snake_positions[index].pop()

def check_collision():
    for i in range(len(snake_positions)):
        if snake_positions[i][0] in snake_positions[i][1:]:
            return True
    return False

def restart_game():
    global snake_positions, food_position, directions, scores, start_time
    snake_positions = [[(WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2)], [(3 * WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2)]]
    food_position = get_random_position()
    directions = [(0, 1), (0, 1)]
    scores = [0, 0]
    start_time = time.time()


def start_1player_game():
    global game_mode, challenge_mode
    game_mode = '1player'
    challenge_mode = False

def start_2player_game():
    global game_mode, challenge_mode
    game_mode = '2player'
    challenge_mode = False

def start_1player_challenge():
    global game_mode, challenge_mode
    game_mode = '1player'
    challenge_mode = True
    set_random_challenge()

def start_2player_challenge():
    global game_mode, challenge_mode
    game_mode = '2player'
    challenge_mode = True
    set_random_challenge()

def show_high_scores():
    global game_mode
    game_mode = 'high_scores'

def set_random_challenge():
    global challenge_goal, challenge_time
    challenge_goal = random.randint(10, 30)
    challenge_time = random.randint(30, 90)



def challenge_complete():
    window.fill(BACKGROUND_COLOR)
    complete_text = title_font.render("YOU WON!", True, (0, 255, 0))
    text_rect = complete_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
    window.blit(complete_text, text_rect)

    draw_button("New Challenge", WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 + 50, 140, 50, (0, 200, 0), (0, 255, 0), new_challenge)
    draw_button("Exit", WINDOW_WIDTH // 2 + 10, WINDOW_HEIGHT // 2 + 50, 140, 50, (200, 0, 0), (255, 0, 0), lambda: setattr(pygame.event.Event(pygame.KEYDOWN), 'key', pygame.K_ESCAPE))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting = False

def new_challenge():
    global challenge_mode, game_mode
    challenge_mode = True
    set_random_challenge()
    restart_game()
    game_loop()

def exit_to_menu():
    global game_mode, challenge_mode
    game_mode = None
    challenge_mode = False