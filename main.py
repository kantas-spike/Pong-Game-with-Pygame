import pygame
import os
import random
import toml

DEFAULT_KEY_UP = pygame.K_w
DEFAULT_KEY_DOWN = pygame.K_s

WIDTH, HEIGHT = 900, 500

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game!")

RETRO_BLUE = (44, 78, 114)

BORDER = pygame.Rect(WIDTH / 2 - 2, 0, 4, HEIGHT)
FPS = 60
VEL = 6

AI_VEL = 6

AI_JUDGE_STARTING_POINT = WIDTH * 0.55

RECTANGLE_WIDTH, RECTANGLE_HEIGHT = 5, 60


RECTANGLE_IMAGE = pygame.image.load(os.path.join("Assets", "red_rectangle.png"))
RECTANGLE = pygame.transform.scale(RECTANGLE_IMAGE, (RECTANGLE_WIDTH, RECTANGLE_HEIGHT))
BALL = pygame.Rect(WIDTH / 2 - 7.5, HEIGHT / 2 - 7.5, 15, 15)


def draw_window(P1, P2):
    WIN.fill(RETRO_BLUE)
    pygame.draw.rect(WIN, (255, 255, 255), BORDER)
    pygame.draw.ellipse(WIN, (255, 255, 255), BALL)
    WIN.blit(RECTANGLE, (P1.x, P1.y))
    WIN.blit(RECTANGLE, (P2.x, P2.y))
    pygame.display.update()


def P1_handle_movement(keys_pressed, P1, key_up=DEFAULT_KEY_UP, key_down=DEFAULT_KEY_DOWN):
    if keys_pressed[key_up]:  # P1 UP
        if P1.y > 10:
            P1.y -= VEL

    if keys_pressed[key_down]:  # P1 DOWN
        if P1.y < HEIGHT - 10 - RECTANGLE_HEIGHT:
            P1.y += VEL


def BALL_restart(ball_vel_x, ball_vel_y):
    BALL.center = (WIDTH / 2, HEIGHT / 2)
    ball_vel_y *= random.choice((1, -1))
    ball_vel_x *= random.choice((1, -1))


def get_config(toml_file="pyproject.toml"):
    pong_settings = toml.load(toml_file).get("pong", {})
    key_settings = pong_settings.get("key", {"up": "K_w", "down": "K_s"})
    const_dict = vars(pygame.constants)
    config = {}
    for k, v in key_settings.items():
        if v not in const_dict:
            raise Exception(f"Invalid {k} key in pong.key: {v}")
        else:
            config[f"key_{k}"] = const_dict[v]

    return config


def expected_ball_position(b_position, d_x, d_y, p2_x):
    slope = d_y / d_x

    c_p = horizontal_contact_point(b_position, slope)
    if c_p[0] < p2_x:
        c_p = vertical_contact_point(p2_x, c_p, slope * -1)
    else:
        c_p = vertical_contact_point(p2_x, b_position, slope)
    return c_p


def horizontal_contact_point(b_position, slope):
    b_x, b_y = b_position
    if slope > 0:
        y = HEIGHT
    else:
        y = 0
    x = (y - b_y) / slope + b_x
    return (x, y)


def vertical_contact_point(p2_x, b_position, slope):
    b_x, b_y = b_position
    y = slope * (p2_x - b_x) + b_y
    return (p2_x, y)


def move_p2(P2, d_x, d_y):
    y = BALL.y
    if d_x > 0 and BALL.x > AI_JUDGE_STARTING_POINT:
        e_p = expected_ball_position((BALL.x, BALL.y), d_x, d_y, P2.x)
        y = e_p[1]
    else:
        y = (HEIGHT - RECTANGLE_HEIGHT) / 2

    if P2.top < y:
        P2.top = min(HEIGHT - 10 - RECTANGLE_HEIGHT, P2.top + AI_VEL)
    if P2.bottom > y:
        P2.bottom = max(10 + RECTANGLE_HEIGHT, P2.bottom - AI_VEL)


def main():
    config = get_config()
    print(config)

    ball_vel_y = 7
    ball_vel_x = 7
    P1 = pygame.Rect(40, 250, RECTANGLE_WIDTH, RECTANGLE_HEIGHT)
    P2 = pygame.Rect(860, 250, RECTANGLE_WIDTH, RECTANGLE_HEIGHT)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        P1_handle_movement(keys_pressed, P1, key_up=config["key_up"], key_down=config["key_down"])
        # BALL MOVEMENT
        BALL.x += ball_vel_x
        BALL.y += ball_vel_y
        if BALL.top <= 0 or BALL.bottom >= HEIGHT:
            ball_vel_y *= -1
        if BALL.left <= 0 or BALL.right >= WIDTH:
            BALL_restart(ball_vel_x, ball_vel_y)

        if BALL.colliderect(P1) or BALL.colliderect(P2):
            ball_vel_x *= -1

        # AI MOVEMENT

        move_p2(P2, ball_vel_x, ball_vel_y)

        draw_window(P1, P2)

    pygame.quit()


if __name__ == "__main__":
    main()
