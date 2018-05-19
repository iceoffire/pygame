import pygame, os
from pygame.locals import *

def main():
    running, settings = load()
    while running:
        settings = update(settings)
        draw(settings)
        running = check_exit()
    pygame.quit()

def load():
    screen_size = (400, 500)
    screen = pygame.display.set_mode(screen_size)
    game_object = {
        'enemy'         : [],
        'kill_effect'   : [],
        'player'        : [],
        'HUD'           : {
            'line'  : [],
            'img'   : [],
            'font'  : []
        }
    }
    var = {
        'folder' : os.path.dirname(os.path.realpath(__file__)),
        'layer'  : ['enemy', 'player', 'kill_effect']
    }
    return True, {
        'screen'        : screen,
        'screen_size'   : screen_size,
        'game_object'   : game_object,
        'var'           : var
    }

def update(settings):
    return settings

def draw(settings):
    draw_gO(settings['screen'], settings['game_object'], settings['var']['layer'])
    draw_HUD(settings['screen'], settings['game_object']['HUD'])

def draw_gO(game_object, layer_order):
    for name in layer_order:
        for gO in game_object[name]:
            screen.blit(gO.img, (gO.x, gO.y))

def draw_HUD(screen, HUD):
    for name in HUD:
        for gO in HUD:
            if gO.__class__ == Line2D:
                pass
            if gO.__class__ == Sprite:
                screen.blit(gO.img, (gO.x, gO.y))
            if gO.__class__ == Font:
                pass

def check_exit():
    k = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type==QUIT or k[K_ESCAPE]:
            return False
    return True

if __name__=='__main__':
    main()