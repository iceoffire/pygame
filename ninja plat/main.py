import pygame, os
from pygame.locals import *
from time import time

def main():
    init = time()
    running, settings = load()
    print(time()-init)
    init = time()
    while running:
        settings = update(settings)
        draw(settings)
        running = check_exit()
    pygame.quit()

def load():
    settings = load_settings()
    settings['game_object'] = load_game_object(settings['game_object'])
    running = True
    return running, settings
    
def load_settings():
    screen_size = (700, 550)
    screen = pygame.display.set_mode(screen_size)
    game_object = {
        'player'    : [],
        'tile'      : [],
        'collider'  : [],
        'bg'        : [],
        'camera'    : []
    }
    vars = {
        'folder'    : os.path.dirname(os.path.realpath(__file__)),
        'total_maps': len(os.listdir(os.path.dirname(os.path.realpath(__file__)) + '/assets/img/map'))

    }
    return {
        'screen_size'   : screen_size,
        'screen'        : screen,
        'game_object'   : game_object,
        'vars'          : vars,
    }

def load_game_object(game_object):
    #game_object['player'].append(Sprite(x, y, width, height, collider, animation( \
    #               {'idle' :  2, 'running' : 4, 'attack' : 3}, '/assets/img/player'))
    return game_object