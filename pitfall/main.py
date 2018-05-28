import pygame
from pygame.locals import QUIT, K_ESCAPE, K_a, K_d, K_s, K_SPACE
from time import time
from os.path import dirname, realpath
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
        'wall'          : [],
    }

    var = {
        'folder'        : dirname(realpath(__file__)),
        'level'         : 1,
        'seconds_left'  : 1200,
        'hp'            : 2000,
        'lifes'         : 3,
        'exit'          : False
    }

    #game_object['player'].append()

    return True, {
        'screen_size'   : screen_size,
        'screen'        : screen,
        'game_object'   : game_object,
        'var'           : var,
    }

def update(settings):
    return settings

def draw(settings):
    pass

def check_exit(settings):
    if settings['var']['exit']: return False
    k = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == QUIT or k[K_ESCAPE]:
            return False
    return True


class Sprite():
    def __init__(self, x, y, path, collider=None, animation=None, gravity=False):
        self.x              = x
        self.y              = y
        self.path           = path
        self.img            = pygame.image.load(path)
        self.gravity        = gravity
        if collider != None:
            #                         (x          , y          , width      , height     , obj)
            self.collider   = Collider2D(collider[0], collider[1], collider[2], collider[3], self)
        if animation != None:
            #                         (sprites     , path        , first       , obj)
            #sprites = {'anim1' : [qnt, time], 'anim2' : [qnt, time]}
            self.animation  = Animation(animation[0], animation[1], animation[2], self)

class Animation():
    def __init__(self, sprites, path, first, obj):
        self.sprites     = sprites
        self.path        = path
        self.tile        = first
        self.pos         = 0
        self.last_update = time()
        self.obj         = obj
        self.obj.img     = pygame.image.load(path + '/' + first + str(self.pos) + '.png')

    def change(self, tile, pos=0):
        self.tile        = tile
        self.pos         = 0 
        self.obj.img     = pygame.image.load(self.path + '/' + tile + str(pos) + '.png')
    
    def update(self):
        if time()-self.last_update>self.sprites[self.tile][1]:
            if self.pos == self.sprites[self.tile][0]-1:
                self.pos     = 0
            else:
                self.pos    += 1
            self.obj.img     = pygame.image.load(self.path + '/' + self.tile + str(self.pos) + '.png')
            self.last_update = time()

main()