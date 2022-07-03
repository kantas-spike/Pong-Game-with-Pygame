from collections import namedtuple
import pygame
import os
import random
import toml

DEFAULT_KEY_UP = pygame.K_w
DEFAULT_KEY_DOWN = pygame.K_s
COLOR_RETRO_BLUE = (44, 78, 114)
COLOR_WHITE = (255, 255, 255)
FPS = 60
PADDLE1_SPEED = [0, 6]
PADDLE2_SPEED = [0, 6]

SCREEN_SIZE = WIDTH, HEIGHT = 900, 500
AI_JUDGE_STARTING_POINT = WIDTH * 0.65

PADDLE_WIDTH, PADDLE_HEIGHT = 5, 60

Element = namedtuple("Element", ["surface", "rect"])
SCORE = [0, 0]


def setup_score(font, score, point):
    text = font.render(str(score), True, COLOR_WHITE)
    rect = text.get_rect()
    rect.midtop = point
    return Element(surface=text, rect=rect)


def setup_border():
    surface = pygame.Surface((4, HEIGHT))
    surface.fill(COLOR_WHITE)
    element = Element(surface=surface, rect=pygame.Rect(WIDTH / 2 - 2, 0, 4, HEIGHT))
    return element


def setup_ball():
    surface = pygame.Surface((15, 15))
    pygame.draw.ellipse(surface, COLOR_WHITE, (0, 0, 15, 15))
    element = Element(surface=surface, rect=pygame.Rect(WIDTH / 2 - 7.5, HEIGHT / 2 - 7.5, 15, 15))
    return element


def setup_paddle(topleft):
    image = pygame.image.load(os.path.join("Assets", "red_rectangle.png")).convert()
    surface = pygame.transform.scale(image, (PADDLE_WIDTH, PADDLE_HEIGHT))
    rect = pygame.Rect(topleft, (PADDLE_WIDTH, PADDLE_HEIGHT))
    element = Element(surface=surface, rect=rect)
    return element


def draw_screen(screen, border, p1, p2, ball, font):
    screen.fill(COLOR_RETRO_BLUE)
    screen.blit(border.surface, border.rect)

    p1_score_text = setup_score(font, SCORE[0], (WIDTH/4, 10))
    p2_score_text = setup_score(font, SCORE[1], (WIDTH/4 * 3, 10))

    screen.blit(p1_score_text.surface, p1_score_text.rect)
    screen.blit(p2_score_text.surface, p2_score_text.rect)

    screen.blit(p1.surface, p1.rect)
    screen.blit(p2.surface, p2.rect)
    screen.blit(ball.surface, ball.rect)

    pygame.display.flip()


def restart_ball(ball, ball_speed):
    ball.rect.center = (WIDTH / 2, HEIGHT / 2)
    ball_speed[0] *= random.choice((1, -1))
    ball_speed[1] *= random.choice((1, -1))


def get_config(toml_file="pyproject.toml"):
    pong_settings = toml.load(toml_file).get("pong", {})
    key_settings = pong_settings.get("key", {"up": "K_w", "down": "K_s"})
    font_settings = pong_settings.get("font", {"path": "/System/Library/Fonts/Supplemental/Arial.ttf", "size": 24})

    const_dict = vars(pygame.constants)
    config = {}
    for k, v in key_settings.items():
        if v not in const_dict:
            raise Exception(f"Invalid {k} key in pong.key: {v}")
        else:
            config[f"key_{k}"] = const_dict[v]

    config["font_path"] = font_settings["path"]
    config["font_size"] = font_settings["size"]

    return config


def expected_ball_position(b_position, ball_speed, p2_x):
    slope = ball_speed[1] / ball_speed[0]

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


def move_paddle1(keys_pressed, paddle, key_up=DEFAULT_KEY_UP, key_down=DEFAULT_KEY_DOWN):
    if keys_pressed[key_up]:  # P1 UP
        if paddle.rect.top > 10:
            paddle.rect.move_ip(PADDLE1_SPEED[0], PADDLE1_SPEED[1] * -1)

    if keys_pressed[key_down]:  # P1 DOWN
        if paddle.rect.top < HEIGHT - 10 - PADDLE_HEIGHT:
            paddle.rect.move_ip(PADDLE1_SPEED)


def move_paddle2(p2, ball, ball_speed):
    y = ball.rect.y
    if ball_speed[0] > 0 and ball.rect.x > AI_JUDGE_STARTING_POINT:
        e_p = expected_ball_position(ball.rect.topleft, ball_speed, p2.rect.left)
        y = e_p[1]
    else:
        y = (HEIGHT - PADDLE_HEIGHT) / 2

    if p2.rect.top < y:
        p2.rect.top = min(HEIGHT - 10 - PADDLE_HEIGHT, p2.rect.top + PADDLE2_SPEED[1])
    if p2.rect.bottom > y:
        p2.rect.bottom = max(10 + PADDLE_HEIGHT, p2.rect.bottom - PADDLE2_SPEED[1])


def move_ball(ball, ball_speed, p1, p2):
    ball.rect.move_ip(ball_speed)

    if ball.rect.top <= 0 or ball.rect.bottom >= HEIGHT:
        ball_speed[1] *= -1
    if ball.rect.left <= 0 or ball.rect.right >= WIDTH:
        if ball.rect.left <= 0:
            SCORE[1] += 1
        else:
            SCORE[0] += 1

        restart_ball(ball, ball_speed)

    if ball.rect.colliderect(p1.rect) or ball.rect.colliderect(p2.rect):
        ball_speed[0] *= -1


def main():
    config = get_config()

    pygame.init()
    pygame.display.set_caption("Pong Game!")

    font = pygame.font.Font(config["font_path"], config["font_size"])

    screen = pygame.display.set_mode(SCREEN_SIZE)
    border = setup_border()
    ball = setup_ball()
    ball_speed = [7, 7]

    paddle1 = setup_paddle((40, 250))
    paddle2 = setup_paddle((860, 250))

    clock = pygame.time.Clock()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # move elements
        keys_pressed = pygame.key.get_pressed()
        move_paddle1(keys_pressed, paddle1, key_up=config["key_up"], key_down=config["key_down"])
        move_ball(ball, ball_speed, paddle1, paddle2)

        # AI MOVEMENT
        move_paddle2(paddle2, ball, ball_speed)

        # draw
        draw_screen(screen, border, paddle1, paddle2, ball, font)
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
