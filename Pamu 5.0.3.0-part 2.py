def draw_grid():
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        pygame.draw.line(window, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        pygame.draw.line(window, GRID_COLOR, (0, y), (WINDOW_WIDTH, y))

def draw_snake(positions, color):
    snake_body = pygame.Surface((GRID_SIZE, GRID_SIZE))
    snake_body.fill(color)
    snake_body = pygame.transform.scale(snake_body, (GRID_SIZE - 2, GRID_SIZE - 2))

    for position in positions:
        window.blit(snake_body, (position[0] + 1, position[1] + 1))

    head = pygame.Surface((GRID_SIZE, GRID_SIZE))
    head.fill(color)
    head = pygame.transform.scale(head, (GRID_SIZE, GRID_SIZE))
    window.blit(head, positions[0])

    eye1 = pygame.Surface((4, 4))
    eye1.fill((0, 0, 0))
    eye2 = pygame.Surface((4, 4))
    eye2.fill((0, 0, 0))

    direction = directions[0] if color == SNAKE_COLOR_1 else directions[1]
    if direction == (0, -1):  # Up
        window.blit(eye1, (positions[0][0] + 4, positions[0][1] + 4))
        window.blit(eye2, (positions[0][0] + GRID_SIZE - 8, positions[0][1] + 4))
    elif direction == (0, 1):  # Down
        window.blit(eye1, (positions[0][0] + 4, positions[0][1] + GRID_SIZE - 8))
        window.blit(eye2, (positions[0][0] + GRID_SIZE - 8, positions[0][1] + GRID_SIZE - 8))
    elif direction == (-1, 0):  # Left
        window.blit(eye1, (positions[0][0] + 4, positions[0][1] + 4))
        window.blit(eye2, (positions[0][0] + 4, positions[0][1] + GRID_SIZE - 8))
    elif direction == (1, 0):  # Right
        window.blit(eye1, (positions[0][0] + GRID_SIZE - 8, positions[0][1] + 4))
        window.blit(eye2, (positions[0][0] + GRID_SIZE - 8, positions[0][1] + GRID_SIZE - 8))

def draw_food():
    food = pygame.Surface((GRID_SIZE, GRID_SIZE))
    food.fill(FOOD_COLOR)
    food = pygame.transform.scale(food, (GRID_SIZE - 2, GRID_SIZE - 2))
    window.blit(food, (food_position[0] + 1, food_position[1] + 1))

def draw_button(text, x, y, width, height, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(window, hover_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(window, color, (x, y, width, height))

    text_surf = button_font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=(x + width / 2, y + height / 2))
    window.blit(text_surf, text_rect)

def main_menu():
    global game_mode, challenge_mode
    while True:
        window.fill(BACKGROUND_COLOR)
        title_text = title_font.render("Snake Game", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 100))
        window.blit(title_text, title_rect)

        draw_button("1 Player", 300, 200, 200, 50, (0, 200, 0), (0, 255, 0), start_1player_game)
        draw_button("2 Players", 300, 275, 200, 50, (0, 0, 200), (0, 0, 255), start_2player_game)
        draw_button("1P Challenge", 300, 350, 200, 50, (200, 0, 0), (255, 0, 0), start_1player_challenge)
        draw_button("2P Challenge", 300, 425, 200, 50, (200, 0, 200), (255, 0, 255), start_2player_challenge)
        draw_button("High Scores", 300, 500, 200, 50, (200, 200, 0), (255, 255, 0), show_high_scores)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        pygame.display.update()

        if game_mode:
            return

def game_loop():
    global food_position, paused, game_mode, high_scores, challenge_mode, challenge_goal, challenge_time, start_time

    food_position = get_random_position()
    restart_game()

    while True:
        clock.tick(FRAME_RATE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_ESCAPE:
                    game_mode = None
                    return

                if not paused:
                    if game_mode == '1player' or game_mode == '2player':
                        if event.key == pygame.K_UP and directions[0] != (0, 1):
                            directions[0] = (0, -1)
                        elif event.key == pygame.K_DOWN and directions[0] != (0, -1):
                            directions[0] = (0, 1)
                        elif event.key == pygame.K_LEFT and directions[0] != (1, 0):
                            directions[0] = (-1, 0)
                        elif event.key == pygame.K_RIGHT and directions[0] != (-1, 0):
                            directions[0] = (1, 0)

                    if game_mode == '2player':
                        if event.key == pygame.K_w and directions[1] != (0, 1):
                            directions[1] = (0, -1)
                        elif event.key == pygame.K_s and directions[1] != (0, -1):
                            directions[1] = (0, 1)
                        elif event.key == pygame.K_a and directions[1] != (1, 0):
                            directions[1] = (-1, 0)
                        elif event.key == pygame.K_d and directions[1] != (-1, 0):
                            directions[1] = (1, 0)

        if not paused:
            move_snake(0)
            if game_mode == '2player':
                move_snake(1)

            if check_collision():
                crash_sound.play()
                if not challenge_mode:
                    high_scores.append(max(scores))
                    high_scores.sort(reverse=True)
                    high_scores = high_scores[:10]
                    save_high_scores()
                game_over()
                return

        window.fill(BACKGROUND_COLOR)
        draw_grid()
        draw_snake(snake_positions[0], SNAKE_COLOR_1)
        if game_mode == '2player':
            draw_snake(snake_positions[1], SNAKE_COLOR_2)
        draw_food()

        score_text_1 = score_font.render(f"Player 1: {scores[0]}", True, (255, 255, 255))
        window.blit(score_text_1, (10, 10))

        if game_mode == '2player':
            score_text_2 = score_font.render(f"Player 2: {scores[1]}", True, (255, 255, 255))
            window.blit(score_text_2, (WINDOW_WIDTH - 150, 10))

        if challenge_mode:
            time_left = max(0, challenge_time - int(time.time() - start_time))
            challenge_text = score_font.render(f"Goal: {challenge_goal} | Time: {time_left}s", True, (255, 255, 255))
            window.blit(challenge_text, (WINDOW_WIDTH // 2 - 100, 10))

            if time_left == 0:
                challenge_incomplete()
                return
            elif (game_mode == '1player' and scores[0] >= challenge_goal) or (game_mode == '2player' and (scores[0] >= challenge_goal or scores[1] >= challenge_goal)):
                challenge_complete()
                return

        if paused:
            pause_text = pause_font.render("Paused", True, (255, 255, 255))
            text_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            window.blit(pause_text, text_rect)

        pygame.display.update()
def challenge_complete():
    window.fill(BACKGROUND_COLOR)
    complete_text = title_font.render("YOU WON!", True, (0, 255, 0))
    text_rect = complete_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
    window.blit(complete_text, text_rect)

    draw_button("New Challenge", WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 + 50, 200, 50, (0, 200, 0), (0, 255, 0), new_challenge)
    draw_button("Exit", WINDOW_WIDTH // 2 + 60, WINDOW_HEIGHT // 2 + 50, 140, 50, (200, 0, 0), (255, 0, 0), exit_to_menu)

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if WINDOW_WIDTH // 2 - 150 < mouse_pos[0] < WINDOW_WIDTH // 2 + 50 and WINDOW_HEIGHT // 2 + 50 < mouse_pos[1] < WINDOW_HEIGHT // 2 + 100:
                    new_challenge()
                    waiting = False
                elif WINDOW_WIDTH // 2 + 60 < mouse_pos[0] < WINDOW_WIDTH // 2 + 200 and WINDOW_HEIGHT // 2 + 50 < mouse_pos[1] < WINDOW_HEIGHT // 2 + 100:
                    exit_to_menu()
                    waiting = False
def challenge_incomplete():
    window.fill(BACKGROUND_COLOR)
    incomplete_text = title_font.render("YOU LOSE!", True, (255, 0, 0))
    text_rect = incomplete_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
    window.blit(incomplete_text, text_rect)

    draw_button("New Challenge", WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 + 50, 200, 50, (0, 200, 0), (0, 255, 0), new_challenge)
    draw_button("Exit", WINDOW_WIDTH // 2 + 60, WINDOW_HEIGHT // 2 + 50, 140, 50, (200, 0, 0), (255, 0, 0), exit_to_menu)

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if WINDOW_WIDTH // 2 - 150 < mouse_pos[0] < WINDOW_WIDTH // 2 + 50 and WINDOW_HEIGHT // 2 + 50 < mouse_pos[1] < WINDOW_HEIGHT // 2 + 100:
                    new_challenge()
                    waiting = False
                elif WINDOW_WIDTH // 2 + 60 < mouse_pos[0] < WINDOW_WIDTH // 2 + 200 and WINDOW_HEIGHT // 2 + 50 < mouse_pos[1] < WINDOW_HEIGHT // 2 + 100:
                    exit_to_menu()
                    waiting = False

def game_over():
    window.fill(BACKGROUND_COLOR)
    game_over_text = title_font.render("Game Over", True, (255, 0, 0))
    text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
    window.blit(game_over_text, text_rect)

    draw_button("Replay", WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 + 50, 140, 50, (0, 200, 0), (0, 255, 0), restart_game)
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

def show_high_scores_screen():
    while True:
        window.fill(BACKGROUND_COLOR)
        title_text = title_font.render("High Scores", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 50))
        window.blit(title_text, title_rect)

        for i, score in enumerate(high_scores):
            score_text = score_font.render(f"{i + 1}. {score}", True, (255, 255, 255))
            window.blit(score_text, (WINDOW_WIDTH // 2 - 50, 100 + i * 30))

        draw_button("Back", 300, 500, 200, 50, (200, 0, 0), (255, 0, 0), exit_to_menu)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 300 < mouse_pos[0] < 500 and 500 < mouse_pos[1] < 550:
                    return  # This will exit the function and return to the main menu

        pygame.display.update()
