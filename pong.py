import pygame
import sys
import random

pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (30, 30, 30)
COLOR_OPTIONS = {
    "White": WHITE,
    "Red": (255, 0, 0),
    "Blue": (0, 0, 255),
    "Green": (0, 255, 0),
    "Yellow": (255, 255, 0),
}

# Paddle and ball
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
PADDLE_SPEED = 7
BALL_SIZE = 20
BALL_SPEED_X, BALL_SPEED_Y = 7, 7
SCORE_LIMIT = 10

# Fonts
font = pygame.font.SysFont("Arial", 36)
menu_font = pygame.font.SysFont("Arial", 48)
score_font = pygame.font.SysFont("Arial", 72)

# Clock
clock = pygame.time.Clock()

# Game variables
left_score = right_score = 0
game_mode = "single"  # default
ball_color = WHITE
left_color = WHITE
right_color = WHITE

# ----- Helper functions -----
def draw_text_center(text, font, color, y):
    render = font.render(text, True, color)
    rect = render.get_rect(center=(WIDTH // 2, y))
    WINDOW.blit(render, rect)

def main_menu():
    global game_mode, ball_color, left_color, right_color
    selected_option = 0
    color_options = list(COLOR_OPTIONS.keys())
    selected_ball_color = 0
    selected_left_color = 0
    selected_right_color = 0

    while True:
        WINDOW.fill(DARK_GRAY)

        # Animated floating rectangles as background
        for _ in range(15):
            x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
            pygame.draw.rect(WINDOW, (50, 50, 50), (x, y, 2, 2))

        draw_text_center("PONG", menu_font, WHITE, 100)

        options = [
            f"Mode: {'Single Player' if game_mode=='single' else 'Two Players'}",
            f"Ball Color: {color_options[selected_ball_color]}",
            f"Left Paddle Color: {color_options[selected_left_color]}",
            f"Right Paddle Color: {color_options[selected_right_color]}",
            "Press Enter to Start",
        ]

        for i, option in enumerate(options):
            color = WHITE if i == selected_option else (150, 150, 150)
            draw_text_center(option, font, color, 200 + i*60)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                if event.key == pygame.K_LEFT:
                    if selected_option == 0:
                        game_mode = "single" if game_mode != "single" else "double"
                    elif selected_option == 1:
                        selected_ball_color = (selected_ball_color - 1) % len(color_options)
                    elif selected_option == 2:
                        selected_left_color = (selected_left_color - 1) % len(color_options)
                    elif selected_option == 3:
                        selected_right_color = (selected_right_color - 1) % len(color_options)
                if event.key == pygame.K_RIGHT:
                    if selected_option == 0:
                        game_mode = "single" if game_mode != "single" else "double"
                    elif selected_option == 1:
                        selected_ball_color = (selected_ball_color + 1) % len(color_options)
                    elif selected_option == 2:
                        selected_left_color = (selected_left_color + 1) % len(color_options)
                    elif selected_option == 3:
                        selected_right_color = (selected_right_color + 1) % len(color_options)
                if event.key == pygame.K_RETURN:
                    # set colors
                    ball_color = COLOR_OPTIONS[color_options[selected_ball_color]]
                    left_color = COLOR_OPTIONS[color_options[selected_left_color]]
                    right_color = COLOR_OPTIONS[color_options[selected_right_color]]
                    return

def draw_game(left_paddle, right_paddle, ball):
    WINDOW.fill(DARK_GRAY)

    # Center line (dashed)
    for y in range(0, HEIGHT, 20):
        pygame.draw.rect(WINDOW, WHITE, (WIDTH//2 - 2, y, 4, 10))

    # Paddles and ball
    pygame.draw.rect(WINDOW, left_color, left_paddle)
    pygame.draw.rect(WINDOW, right_color, right_paddle)
    pygame.draw.ellipse(WINDOW, ball_color, ball)

    # Scores
    left_score_text = score_font.render(str(left_score), True, WHITE)
    right_score_text = score_font.render(str(right_score), True, WHITE)
    WINDOW.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    WINDOW.blit(right_score_text, (WIDTH*3//4 - right_score_text.get_width()//2, 20))

    pygame.display.flip()

def handle_input(left_paddle, right_paddle):
    keys = pygame.key.get_pressed()
    # Left paddle
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += PADDLE_SPEED
    # Right paddle
    if game_mode == "double":
        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
            right_paddle.y += PADDLE_SPEED

def ai_move(ball, right_paddle):
    if ball.centery > right_paddle.centery and right_paddle.bottom < HEIGHT:
        right_paddle.y += PADDLE_SPEED
    elif ball.centery < right_paddle.centery and right_paddle.top > 0:
        right_paddle.y -= PADDLE_SPEED

def move_ball(ball, ball_vel, left_paddle, right_paddle):
    global left_score, right_score
    ball.x += ball_vel[0]
    ball.y += ball_vel[1]

    # Bounce off top/bottom
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_vel[1] *= -1

    # Bounce off paddles
    if ball.colliderect(left_paddle) and ball_vel[0] < 0:
        ball_vel[0] *= -1
    if ball.colliderect(right_paddle) and ball_vel[0] > 0:
        ball_vel[0] *= -1

    # Score
    if ball.left <= 0:
        right_score += 1
        reset_ball(ball, ball_vel)
    if ball.right >= WIDTH:
        left_score += 1
        reset_ball(ball, ball_vel)

def reset_ball(ball, ball_vel):
    ball.center = (WIDTH//2, HEIGHT//2)
    ball_vel[0] = BALL_SPEED_X * random.choice([-1, 1])
    ball_vel[1] = BALL_SPEED_Y * random.choice([-1, 1])

def game_over():
    global left_score, right_score
    winner = "Left Player" if left_score == SCORE_LIMIT else "Right Player"
    if game_mode == "single" and winner == "Right Player":
        winner = "AI"
    while True:
        WINDOW.fill(DARK_GRAY)
        draw_text_center(f"{winner} Wins!", menu_font, WHITE, HEIGHT//2)
        draw_text_center("Press Enter to return to menu", font, WHITE, HEIGHT//2 + 80)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                left_score = right_score = 0
                return

# ----- Main Game Loop -----
while True:
    main_menu()
    left_paddle = pygame.Rect(50, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
    ball_vel = [BALL_SPEED_X * random.choice([-1, 1]), BALL_SPEED_Y * random.choice([-1, 1])]

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        handle_input(left_paddle, right_paddle)
        if game_mode == "single":
            ai_move(ball, right_paddle)

        move_ball(ball, ball_vel, left_paddle, right_paddle)
        draw_game(left_paddle, right_paddle, ball)

        if left_score == SCORE_LIMIT or right_score == SCORE_LIMIT:
            running = False
            game_over()