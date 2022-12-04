import pygame
from pygame.locals import *
from math import sin,cos
import math


def main():
    settings, playing = load()
    while playing:
        settings = update(settings)
        draw(**settings)
        playing = check_exit(settings['exit'])
    pygame.quit()

def load():
    screen_size = (400, 400)
    scene = pygame.display.set_mode(screen_size)
    ball = GameObject(30, 250, 20)
    pygame.font.init()
    return {
        'screen' : scene,
        'ball' : ball,
        'exit' : False,
        'font': pygame.font.SysFont("arial", 20),
    }, True

def update(settings):
    k = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == QUIT or k[K_ESCAPE]:
            settings['exit'] = True
        if k[K_r]:
            settings['ball'].x = 30
            settings['ball'].y = 250
            settings['ball'].gravity = False
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            pos = pygame.mouse.get_pos()
            if settings['ball'].gravity == False: # is ball stoped?
                settings['ball'].gravity = True 
                hypotenuse = (((settings['ball'].x-pos[0])**2)+((settings['ball'].y-pos[1])**2))**0.5
                # calculate mouse direction and
                settings['ball'].delta_x = (-hypotenuse/10.0)*sin(math.atan2(settings['ball'].x-pos[0], settings['ball'].y-pos[1]))
                settings['ball'].delta_y = (-hypotenuse/10.0)*cos(math.atan2(settings['ball'].x-pos[0], settings['ball'].y-pos[1]))
    if settings['ball'].gravity:
        settings['ball'].x += settings['ball'].delta_x # update positions
        settings['ball'].y += settings['ball'].delta_y
        settings['ball'].delta_y += 1 # accelerate Y axis
        settings['ball'].delta_x *= 0.98 # slow the ball in the X axis
            
    return settings

def draw(screen, ball, font, **kwargs):
    m_pos = pygame.mouse.get_pos()
    screen.fill((0,0,0))
    pygame.draw.aaline(screen, (255,255,0), (30, 250), (m_pos[0], m_pos[1]))
    pygame.draw.circle(screen, (255,255,255), (int(ball.x), int(ball.y)), ball.raio)
    screen.blit(font.render('Press "R" to Reset', True, (255, 255, 255)), (10, 10))
    pygame.display.flip()
    fps(60)
    pass

def fps(frames):
    pygame.time.Clock().tick(frames)

def check_exit(exit_r):
    return not exit_r

class GameObject:
    def __init__(self, x, y, raio):
        self.x = x
        self.y = y
        self.delta_x = 0
        self.delta_y = 0
        self.raio = raio
        self.gravity = False

if __name__=='__main__':
    main()
