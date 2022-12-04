import pygame
from pygame.locals import *
from math import sin, cos, radians
from os.path import realpath, dirname

def main():
    running, settings = load()
    while running:
        settings = update(settings)
        draw(settings)
        running = check_exit(settings)
    pygame.quit()

def load():
    screen_size = (200, 200)
    screen = pygame.display.set_mode(screen_size)
    foto = pygame.image.load(dirname(realpath(__file__))+'/teste.jpg')
    foto = pygame.transform.scale(foto, screen_size)
    var = {
        'exit_request'  : False,
        'offset'        : 0,
    }
    return True, {
        'screen_size'   : screen_size,
        'screen'        : screen,
        'foto'          : foto,
        'var'           : var,
    }

def update(settings):
    return settings

def draw(settings):
    
    settings['screen'].blit(settings['foto'], (0, 0))
    update_shader(settings['screen'], settings['var']['offset'])
    pygame.display.flip()
    settings['var']['offset'] = ((pygame.time.get_ticks()/30)%100)
    pygame.time.Clock().tick(1000)
    pass


def update_shader(surface, time):
    for row in range(surface.get_height()):
        for column in range(surface.get_width()):
            if (row+column/3+time*time)%100 and (row*column)%200>80:
                rgba = [x/5 for x in surface.get_at((column, row))]
                
                surface.set_at((column, row), rgba)

def check_exit(settings):
    if settings['var']['exit_request']:
        return False
    k = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == QUIT or k[K_ESCAPE]:
            return False
    return True

main()
