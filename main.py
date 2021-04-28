import random

import pygame
import sys

pygame.init()
clock = pygame.time.Clock()


class Pong:
    def __init__(self):
        self.screen_width = 1080
        self.screen_height = 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pong")

        self.light_grey = (200, 200, 200)
        self.bg_color = pygame.Color('grey12')

        self.ball = pygame.Rect(self.screen_width / 2 - 15, self.screen_height / 2 - 15, 30, 30)
        self.player = pygame.Rect(self.screen_width - 20, self.screen_height / 2 - 70, 10, 140)
        self.opponent = pygame.Rect(10, self.screen_height / 2 - 70, 10, 140)

        self.ball_x_speed = 8 * random.choice((1, -1))
        self.ball_y_speed = 8 * random.choice((1, -1))

        self.player_speed = 0
        self.opponent_speed = 6

        self.player_score = 0
        self.opponent_score = 0

        self.score_time = True

        self.game_font = pygame.font.Font("freesansbold.ttf", 50)

    # drawing player , opponent, ball and a line
    def draw_objects(self):

        self.screen.fill(self.bg_color)
        pygame.draw.rect(self.screen, self.light_grey, self.player)
        pygame.draw.rect(self.screen, self.light_grey, self.opponent)
        pygame.draw.ellipse(self.screen, self.light_grey, self.ball)
        pygame.draw.aaline(self.screen, self.light_grey, (self.screen_width / 2, 0),
                           (self.screen_width / 2, self.screen_height))

    # ball movement
    def ball_animation(self):

        self.ball.x += self.ball_x_speed
        self.ball.y += self.ball_y_speed

        # if ball goes out of the frame , change its direction
        if self.ball.top <= 0 or self.ball.bottom >= self.screen_height:
            self.ball_y_speed *= -1

        if self.ball.left <= 0:
            self.score_time = pygame.time.get_ticks()
            self.player_score += 1

        if self.ball.right >= self.screen_width:
            self.score_time = pygame.time.get_ticks()
            self.opponent_score += 1

        # if ball collides player or opponent , change its direction
        if self.ball.colliderect(self.player) or self.ball.colliderect(self.opponent):
            self.ball_x_speed *= -1

    def player_animation(self):
        self.player.y += self.player_speed

        # if player top reaches top
        if self.player.top <= 0:
            self.player.top = 0
        if self.player.bottom >= self.screen_height:
            self.player.bottom = self.screen_height

    # opponent movement
    def opponent_animation(self):

        # moving opponent up-down w.r.t ball
        if self.opponent.top < self.ball.y:
            self.opponent.y += self.opponent_speed
        if self.opponent.bottom > self.ball.y:
            self.opponent.y -= self.opponent_speed

        if self.opponent.top <= 0:
            self.opponent.top = 0
        if self.opponent.bottom >= self.screen_height:
            self.opponent.bottom = self.screen_height

    # when player or opponent scores, shift ball to center and randomise its initial direction
    def ball_start(self):
        self.ball.center = (self.screen_width / 2, self.screen_height / 2)

        # checking  after goal is scored if 2-3 secs are passed or not
        current_time = pygame.time.get_ticks()

        # 3
        if (current_time - self.score_time) < 800:
            num_3 = self.game_font.render("3", False, self.light_grey)
            self.screen.blit(num_3, (self.screen_width / 2 - 10, self.screen_height / 2 + 20))
            # print(3)

        # 2
        if (current_time - self.score_time) < 1600:
            num_2 = self.game_font.render("2", False, self.light_grey)
            self.screen.blit(num_2, (self.screen_width / 2 - 10, self.screen_height / 2 + 20))

        # 1
        if (current_time - self.score_time) < 2400:
            num_1 = self.game_font.render("1", False, self.light_grey)
            self.screen.blit(num_1, (self.screen_width / 2 - 10, self.screen_height / 2 + 20))

        if (current_time - self.score_time) < 2400:
            # making speeds 0 so ball won't move
            self.ball_x_speed = 0
            self.ball_y_speed = 0
        else:
            # if 2-3 secs are passed make ball move
            self.ball_x_speed = 8 * random.choice((1, -1))
            self.ball_y_speed = 8 * random.choice((1, -1))
            self.score_time = None

    # displaying score
    def print_score(self):

        score = self.game_font.render("Score :", False, self.light_grey)
        self.screen.blit(score, (320, 17))
        player_text = self.game_font.render(f"{self.player_score}", False, self.light_grey)
        self.screen.blit(player_text, (550, 20))
        opponent_text = self.game_font.render(f"{self.opponent_score}", False, self.light_grey)
        self.screen.blit(opponent_text, (500, 20))


pong = Pong()
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pong.player_speed -= 7
            if event.key == pygame.K_DOWN:
                pong.player_speed += 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                pong.player_speed += 7
            if event.key == pygame.K_DOWN:
                pong.player_speed -= 7

    if pong.score_time:
        pong.ball_start()
    pong.ball_animation()
    pong.player_animation()
    pong.opponent_animation()
    pong.draw_objects()

    pong.print_score()

    # Updating the entire window
    pygame.display.flip()
    clock.tick(60)
