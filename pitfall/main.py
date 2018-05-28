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
    scale = 1
    screen_size = (320*scale, 210*scale)
    #screen_size = (640, 420)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('pitfall replica - ULISSES GANDINI')
    pygame.font.init()
    game_object = {
        'HUD'           : [],
        'player'        : [],
        'crocodile'     : [],
        'scorpion'      : [],
        'vine'          : [],
        'wood'          : [],
        'serpent'       : [],
        'bg'            : [],
        'ladder'        : [],
        'water'         : [],
        'hole'          : [],
        'water_croco'   : [],
        'wall'          : [],
        'floor'         : []   
    }

    var = {
        'folder'        : dirname(realpath(__file__)),
        'level'         : 1,
        'seconds_left'  : 1200,
        'hp'            : 2000,
        'lifes'         : 3,
        'exit'          : False,
        'init'          : time(),
        'layer'         : ['bg', 'ladder', 'floor', 'wall', 'water', 'hole', 'water_croco', 'wood', 'vine', 'HUD', 'player'],
        'scale'         : scale
    }

    sprite = {
        'idle'      : [1, 0],
        'running'   : [5, 0.3],
        'vine'      : [1, 0],
        'jumping'   : [1, 0],
        'climbing'  : [2, 0]
    }

    #loading first map
    game_object['player'].append(Sprite(30, 110, var['folder']+'/assets/img/player/idle0.png', (30, 380, 16, 22), \
        (sprite, var['folder'] + '/assets/img/player', 'idle')))

    game_object['bg'].append(Sprite(16, 13, var['folder']+'/assets/img/bg/bg.png'))

    game_object['floor'].append(Sprite(16, 124, var['folder']+'/assets/img/floor/floor.png'))

    game_object['wall'].append(Sprite(280, 155, var['folder']+'/assets/img/wall/wall.png'))
    
    game_object['ladder'].append(Sprite(156, 140, var['folder']+'/assets/img/ladder/ladder.png'))

    game_object['wood'].append(Sprite(260, 123, var['folder']+'/assets/img/wood/wood0.png'))

    return True, {
        'screen_size'   : screen_size,
        'screen'        : screen,
        'game_object'   : game_object,
        'var'           : var,
    }

def update(settings):
    settings['var']['seconds_left'] = 1201-(time()-settings['var']['init'])
    return settings

def draw(settings):
    mm = int(settings['var']['seconds_left']//60)
    ss = int(settings['var']['seconds_left']%60)
    if len(str(ss))==1: ss = '0' + str(ss)
    time = str(mm) + ':' + str(ss)
    hp = str(settings['var']['hp'])

    game_object = settings['game_object']
    layer = settings['var']['layer']
    screen = settings['screen']
    screen.fill((0, 0, 0))
    scale = settings['var']['scale']
    for name in layer:
        for gO in game_object[name]:
            if gO.__class__==Sprite:
                temp_img = pygame.transform.scale(gO.img, (gO.img.get_width()*scale, gO.img.get_height()*scale))
                screen.blit(temp_img, (gO.x*scale, gO.y*scale))
    font = pygame.font.SysFont("PressStart2P", 15)
    
    screen.blit(font.render(hp, True, (230, 230, 230)), (75, 17))
    screen.blit(font.render(time, True, (230, 230, 230)), (60, 33))
    pygame.display.flip()
    pass

def check_exit(settings):
    if settings['var']['exit']: return False
    k = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == QUIT or k[K_ESCAPE]:
            return False
    return True


class Sprite():
    def __init__(self, x, y, path, collider=None, animation=None):
        self.x              = x
        self.y              = y
        self.path           = path
        self.img            = pygame.image.load(path)
        if collider != None:
            #                         (x          , y          , width      , height     , obj)
            self.collider   = Collider2D(collider[0], collider[1], collider[2], collider[3], self)
        if animation != None:
            #                         (sprites     , path        , first       , obj)
            #sprites = {'anim1' : [amount, time], 'anim2' : [amount, time]}
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

class Collider2D():
    def __init__(self, x, y, width, height, obj):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.obj = obj

main()