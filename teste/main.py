import pygame
from Box2D import Box2D
from pygame.locals import *

def main():
    running = load()
    while running:
        update()
        draw()
        running = check_exit()
    pygame.quit()

def load():
    global screen_size, screen, game_object
    screen_size = (400, 400)
    screen = pygame.display.set_mode(screen_size)
    game_object = {
        'cube' : [Box2D(185, 185, 30, 30)]
    }
    return True

def update():
    k = pygame.key.get_pressed()
    if k[K_d]:
        Box2D.move()
    pass

def draw():
    screen.fill((0, 0, 0))
    for name in game_object:
        for gO in game_object[name]:
            pygame.draw.rect(screen, (255, 255, 255), (gO.x, gO.y, gO.w, gO.h))
    pygame.display.flip()

def check_exit():
    k = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type==QUIT or k[K_ESCAPE]:
            return False
    return True

main()