import pygame
import os
import random
import toml
from abc import ABC, abstractstaticmethod

DEFAULT_KEY_UP = pygame.K_w
DEFAULT_KEY_DOWN = pygame.K_s
DEFAULT_FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"
DEFAULT_FONT_SIZE = 24

COLOR_RETRO_BLUE = (44, 78, 114)
COLOR_WHITE = (255, 255, 255)
FPS = 60
SCREEN_SIZE = WIDTH, HEIGHT = 900, 500


class Drawable(ABC):
    @abstractstaticmethod
    def draw(self, screen):
        pass


class Ball(Drawable):
    def __init__(self, ball_speed) -> None:
        self.surface = pygame.Surface((15, 15))
        pygame.draw.ellipse(self.surface, COLOR_WHITE, (0, 0, 15, 15))
        self.rect = pygame.Rect(WIDTH / 2 - 7.5, HEIGHT / 2 - 7.5, 15, 15)
        self.speed = ball_speed

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

    def move(self, p1, p2):
        self.rect.move_ip(self.speed)

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed[1] *= -1

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            return False

        if self.rect.colliderect(p1.rect) or self.rect.colliderect(p2.rect):
            self.speed[0] *= -1

        return True

    def restart(self):
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.speed[0] *= random.choice((1, -1))
        self.speed[1] *= random.choice((1, -1))

    def expected_ball_position(self, x_paddle, paddle_type):
        slope = self.speed[1] / self.speed[0]

        c_p = self.horizontal_contact_point(slope)
        if paddle_type == "right" and c_p[0] < x_paddle:
            c_p = self.vertical_contact_point(x_paddle, c_p, slope * -1)
        elif paddle_type == "left" and c_p[0] > x_paddle:
            c_p = self.vertical_contact_point(x_paddle, c_p, slope * -1)
        else:
            c_p = self.vertical_contact_point(x_paddle, self.rect.topleft, slope)
        return c_p

    def horizontal_contact_point(self, slope):
        b_x, b_y = self.rect.topleft
        if slope > 0:
            y = HEIGHT
        else:
            y = 0
        x = (y - b_y) / slope + b_x
        return (x, y)

    def vertical_contact_point(self, x_paddle, position, slope):
        b_x, b_y = position
        y = slope * (x_paddle - b_x) + b_y
        return (x_paddle, y)


class Paddle(Drawable):
    AI_JUDGE_STARTING_POINT = WIDTH * 0.65
    PADDLE_WIDTH = 5
    PADDLE_HEIGHT = 60

    def __init__(self, topleft, speed) -> None:
        image = pygame.image.load(os.path.join("Assets", "red_rectangle.png")).convert()
        self.surface = pygame.transform.scale(image, (self.PADDLE_WIDTH, self.PADDLE_HEIGHT))
        self.rect = pygame.Rect(topleft, (self.PADDLE_WIDTH, self.PADDLE_HEIGHT))
        self.speed = speed
        if self.rect.left > WIDTH / 2:
            self.__paddle_type = "right"
        else:
            self.__paddle_type = "left"

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

    def move_by_manual(self, keys_pressed, key_up=DEFAULT_KEY_UP, key_down=DEFAULT_KEY_DOWN):
        if keys_pressed[key_up]:  # P1 UP
            if self.rect.top > 10:
                self.rect.move_ip(self.speed[0], self.speed[1] * -1)

        if keys_pressed[key_down]:  # P1 DOWN
            if self.rect.top < HEIGHT - 10 - self.PADDLE_HEIGHT:
                self.rect.move_ip(self.speed)

    def move_by_auto(self, ball):
        y = ball.rect.y
        if self.__paddle_type == "right" and ball.speed[0] > 0 and ball.rect.x > self.AI_JUDGE_STARTING_POINT:
            e_p = ball.expected_ball_position(self.rect.left, self.__paddle_type)
            y = e_p[1]
        elif (
            self.__paddle_type == "left" and ball.speed[0] < 0 and ball.rect.x > (WIDTH - self.AI_JUDGE_STARTING_POINT)
        ):
            e_p = ball.expected_ball_position(self.rect.left, self.__paddle_type)
            y = e_p[1]
        else:
            y = (HEIGHT - self.PADDLE_HEIGHT) / 2

        if self.rect.top < y:
            self.rect.top = min(HEIGHT - 10 - self.PADDLE_HEIGHT, self.rect.top + self.speed[1])
        if self.rect.bottom > y:
            self.rect.bottom = max(10 + self.PADDLE_HEIGHT, self.rect.bottom - self.speed[1])


class Score(Drawable):
    def __init__(
        self,
        font_path=DEFAULT_FONT_PATH,
        font_size=DEFAULT_FONT_SIZE,
        p1_point=(WIDTH / 4, 10),
        p2_point=(WIDTH / 4 * 3, 10),
    ) -> None:
        self.__font = pygame.font.Font(font_path, font_size)
        self.player_score = [0, 0]
        self.__p1_point = p1_point
        self.__p2_point = p2_point

    def update(self, ball):
        if ball.rect.left <= 0:
            self.player_score[1] += 1
        else:
            self.player_score[0] += 1

    def get_score_text(self, score, point):
        text = self.__font.render(str(score), True, COLOR_WHITE)
        rect = text.get_rect()
        rect.midtop = point
        return (text, rect)

    def draw(self, screen):
        p1_score_text = self.get_score_text(self.player_score[0], self.__p1_point)
        p2_score_text = self.get_score_text(self.player_score[1], self.__p2_point)

        screen.blit(p1_score_text[0], p1_score_text[1])
        screen.blit(p2_score_text[0], p2_score_text[1])


class Border(Drawable):
    def __init__(self, position, size, color=COLOR_WHITE) -> None:
        self.surface = pygame.Surface(size)
        self.surface.fill(color)
        self.rect = pygame.Rect(position, size)

    def draw(self, screen):
        screen.blit(self.surface, self.rect)


def draw_screen(screen, drawable_list):
    screen.fill(COLOR_RETRO_BLUE)

    for d in drawable_list:
        d.draw(screen)

    pygame.display.flip()


def get_config(toml_file="pyproject.toml"):
    pong_settings = toml.load(toml_file).get("pong", {})
    key_settings = pong_settings.get("key", {"up": "K_w", "down": "K_s"})
    font_settings = pong_settings.get("font", {"path": DEFAULT_FONT_PATH, "size": DEFAULT_FONT_SIZE})

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


def main():
    config = get_config()

    pygame.init()
    pygame.display.set_caption("Pong Game!")

    screen = pygame.display.set_mode(SCREEN_SIZE)
    border = Border((WIDTH / 2 - 2, 0), (4, HEIGHT))
    ball = Ball([7, 7])
    paddle1 = Paddle((40, 250), [0, 6])
    paddle2 = Paddle((860, 250), [0, 6])
    score = Score(font_path=config["font_path"], font_size=config["font_size"])

    drawable_list = [border, ball, paddle1, paddle2, score]

    clock = pygame.time.Clock()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # move elements
        keys_pressed = pygame.key.get_pressed()
        paddle1.move_by_manual(keys_pressed, key_up=config["key_up"], key_down=config["key_down"])
        if not ball.move(paddle1, paddle2):
            score.update(ball)
            ball.restart()

        # AI MOVEMENT
        paddle2.move_by_auto(ball)

        # draw
        draw_screen(screen, drawable_list)
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
