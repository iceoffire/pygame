import pygame
from pygame.locals import *

from os.path import realpath, dirname

def main():
    running, settings = load()
    while running:
        settings = update(settings)
        draw(**settings)
        running = check_exit(**settings)
    pygame.quit()
    quit()

def alpha(surface):
    for i in range(surface.get_height()):
        for j in range(surface.get_width()):
            surface.set_at((j,i), (0,0,0,0))
    return surface

def load():
    screen_size = (500, 500)
    screen = pygame.display.set_mode(screen_size)
    surface = load_map(pygame.image.load(dirname(realpath(__file__))+ "/cloud.jpeg"))
    return True, {
        'screen_size'   : screen_size,
        'screen'        : screen,
        'surface'       : surface,
        'exit_request'  : False
    }

def load_map(mask):
    surface = pygame.Surface((mask.get_width(), mask.get_height()))
    for row in range(mask.get_height()):
        for column in range(mask.get_width()):
            color = mask.get_at((column, row))
            if color[1]>200:
                temp_color = (240,240,240)
            elif color[1]>150:
                temp_color = (68,47,27)
            elif color[1]>100:
                temp_color = (33,104,33)
            elif color[1]>80:
                temp_color = (213,220,140)
            else:
                temp_color = (131,186,255)
            surface.set_at((column,row), temp_color)
    return surface

def update(settings):
    print(pygame.time.get_ticks())
    for e in pygame.event.get():
        if e.type == QUIT or (e.type==KEYDOWN and e.key==K_ESCAPE):
            settings['exit_request'] = True
    return settings

def draw(screen, surface, **kwargs):
    screen.fill((0,0,0))
    screen.blit(surface, (0,0))
    pygame.display.flip()
    pygame.time.Clock().tick(60)

def check_exit(exit_request, **kwargs):
    return not exit_request

main()
