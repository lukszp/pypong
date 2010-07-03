SCREEN_SIZE = (640, 400)
BACKGROUND_FILE = 'background.jpg'
RADIUS = 5

import pygame
import time
from pygame.locals import *

PLAYER1_KEYUP = K_w
PLAYER1_KEYDOWN = K_s
PLAYER2_KEYUP = K_UP
PLAYER2_KEYDOWN = K_DOWN
PLATE_WIDTH = 10
PLATE_HEIGHT = 80
BALL_SPEED = 150
PLATE_SPEED = 450
ADDITIONAL_SPEED = 150
SCORE = 5

from random import randint
from random import random

from vector2 import Vector2

#########################################
############################################

class ScoreBoard:

    def __init__(self):
        self.left_score = SCORE
        self.right_score = SCORE
        self.font = pygame.font.SysFont("arial", 24)
        self.pos_left = (10, 10)
        w, h = SCREEN_SIZE
        self.pos_right = (w-30, 10)

    def left_down(self):
        self.left_score += -1
        
    def right_down(self):
        self.right_score += -1

    def render(self, surface):
      
        font = pygame.font.SysFont("arial", 24)
        surface.blit( font.render(str(self.left_score),  True, (0, 0, 0)), self.pos_left)
        surface.blit( font.render(str(self.right_score),  True, (0, 0, 0)), self.pos_right)                        

class Ball:

    'Ball(x,y, radius) -> Ball'

    def __init__(self, x, y, radius, speed = 250):
        'Initialize the Ball object.'

        self.pos = Vector2(x,y)
        self.vel = Vector2(randint(-100,100), randint(-100,100))
        self.initial_speed = speed
        self.speed = speed

    def process(self, time_passed):

        self.pos += self.vel.get_normalised()*time_passed * self.speed
        self.speed += 1
        if self.speed > self.initial_speed + ADDITIONAL_SPEED:
            self.speed -= 1
    
    def render(self, surface):
        x,y = self.pos
        pygame.draw.circle(surface, (0, 0, 255), (int(x), int(y)), RADIUS)

class Plate(object):
    
    def __init__(self, x, y, player_kup, player_kdown, speed):
        self.player_kup = player_kup
        self.player_kdown = player_kdown
        self.pos = Vector2(x, y)
        self.up = Vector2(0, -1)
        self.down = Vector2(0, 1)
        self.speed = speed

    def process(self, time_passed, pressed_keys):

        if pressed_keys[self.player_kup]:
            self.pos += self.up.get_normalized()*time_passed*self.speed;
        elif pressed_keys[self.player_kdown]:
            self.pos += self.down.get_normalized()*time_passed*self.speed;            

    def render(self, surface):
        x, y = self.pos
        rectangle = pygame.Rect(x - PLATE_WIDTH, y - PLATE_HEIGHT / 2, PLATE_WIDTH, PLATE_HEIGHT)
        pygame.draw.rect(surface, (160,234,110), rectangle)


class Playground(object):

    def __init__(self, ball, plate_left, plate_right, score):

        self.entities = ()
        self.background = pygame.image.load(BACKGROUND_FILE).convert()
        self.ball = ball
        self.plate_left = plate_left
        self.plate_right = plate_right
        self.score = score
        self.winner = 'None'
        self.font = pygame.font.SysFont("arial", 24)

    def render(self, surface):

        surface.blit(self.background, (0, 0))
        if self.winner == 'None':

            self.ball.render(surface)
            self.plate_left.render(surface)
            self.plate_right.render(surface)
            self.score.render(surface)

        else:

            self.render_winner(surface)

    def render_winner(self, surface):

        if self.winner == 'left':
            text = 'Left side has won the game!'
        else:
            text = 'Right side has won the game!'
        surface.blit( self.font.render(text, True, (0, 0, 0)), (10,  10))         
            
    def render_initial(self, surface):
     
        surface.blit(self.background, (0, 0))      
        start_text = "Press F1 to play"
        surface.blit( self.font.render(start_text, True, (0, 0, 0)), (10,  10)) 

    def process(self, time_passed, pressed_keys):

        w,  h = SCREEN_SIZE
        time_passed_seconds = time_passed / 1000.0

        if self.winner == 'None':

            self.ball.process(time_passed_seconds)
            if self.collision_detection() != True:
                self.ball.pos = Vector2(int(w/2),int(h/2))
                self.ball.vel = Vector2(randint(0, w-1), randint(0, h-1))
            self.plate_left.process(time_passed_seconds, pressed_keys)
            self.plate_right.process(time_passed_seconds, pressed_keys)

        if self.score.left_score < 1:
            self.winner = 'right'
        elif self.score.right_score < 1:
            self.winner = 'left'

    def collision_detection(self):

        w,  h = SCREEN_SIZE

        if self.ball.pos.x <= 0 + RADIUS + PLATE_WIDTH :

            if self.ball.pos.y <= self.plate_left.pos.y - PLATE_HEIGHT / 2 or self.ball.pos.y >= self.plate_left.pos.y + PLATE_HEIGHT / 2:
                if self.ball.pos.x <= 0:
                    self.score.left_down()
                    return False
            else:
                self.ball.vel.x = -self.ball.vel.x
#                self.ball.vel.y = -self.ball.vel.y


        elif self.ball.pos.x >= w - RADIUS - PLATE_WIDTH - 1:
            if self.ball.pos.y <= self.plate_right.pos.y - PLATE_HEIGHT / 2 or self.ball.pos.y >= self.plate_right.pos.y + PLATE_HEIGHT / 2:
                if self.ball.pos.x >= w:
                    self.score.right_down()
                    return False
            else:
                self.ball.vel.x = -self.ball.vel.x
#                self.ball.vel.y = -self.ball.vel.y
        
        elif  self.ball.pos.y <= 0 + RADIUS:
            self.ball.vel.y = -self.ball.vel.y
 #           self.ball.vel.x = -self.ball.vel.x
        
        elif self.ball.pos.y >= h - RADIUS - 1:
            self.ball.vel.y = -self.ball.vel.y
   #         self.ball.vel.x = -self.ball.vel.x

        print self.ball.vel

        return True

def game_init():

    w, h = SCREEN_SIZE

    ball = Ball(int(w/2), int(h/2), RADIUS, BALL_SPEED);
    plate_left = Plate(PLATE_WIDTH, int(h/2), PLAYER1_KEYUP,PLAYER1_KEYDOWN, PLATE_SPEED)
    plate_right = Plate(w, int(h/2), PLAYER2_KEYUP, PLAYER2_KEYDOWN, PLATE_SPEED)
    score = ScoreBoard()

    playground = Playground(ball, plate_left, plate_right, score)

    return playground

def run():

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
    pygame.display.set_caption("CIPONG")
    pygame.mouse.set_visible(False)

    playground = game_init()

    clock = pygame.time.Clock()

    #ball_image = pygame.image.load("ball.jpg").convert_alpha()
    #plate_image = pygame.image.load("plate.jpg").convert_alpha()

    action = 'stop'

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                return

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_F1]:
            playground = game_init()
            action = 'start' 
        elif pressed_keys[K_ESCAPE]:
            action = 'stop'

        if action == 'start':
            time_passed = clock.tick(50)
            playground.process(time_passed, pressed_keys)
            playground.render(screen)

        else:
            playground.render_initial(screen)

        pygame.display.update()

if __name__ == "__main__":
    run()
