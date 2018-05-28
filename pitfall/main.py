import pygame, osm time
from pygame.locals import *


def main():
    running, settings = load()
    while running:
        settings = update(settings)
        draw(settings)
        running = check_exit(settings)
    pygame.quit()

def load():
    screen_size = (672, 420)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('pitfall replica - ULISSES GANDINI')
    game_object = {
        'HUD'           : [],
        'player'        : [],
        'crocodile'     : [],
        'scorpion'      : [],
        'vine'          : [],
        'wood'          : [],
        'python'        : [],
        'bg'            : [],
        'ladder'        : [],
        'water'         : [],
        'hole'          : [],
        'water_croco'   : [],
    }

    var = {
        'folder'        : os.path.dirname(os.path.realpath(__file__)),
        'level'         : 1,
        'seconds_left'  : 1200,
        'hp'            : 2000,
        'lifes'         : 3,
        
    }
