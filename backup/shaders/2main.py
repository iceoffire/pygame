import pygame
from pygame.locals import *
from time import time
from os.path import dirname, realpath
from random import randint

def main():
    tempo = time()
    maior_update = 0
    maior_draw = 0
    maior_running = 0
    soma_update = 0
    soma_draw = 0
    soma_running = 0
    quant = 0
    running, settings = load()
    print("load: %.4f" %(time()-tempo))
    while running:
        quant+=1
        init = time()
        #settings = update(settings)
        settings = update(settings)

        if time()-init>maior_update:
            maior_update = time()-init
        soma_update += time()-init
        init = time()

        draw(settings)

        if time()-init>maior_draw:
            maior_draw = time()-init
        soma_draw += time()-init
        init = time()

        running = check_exit(settings)

        if time()-init>maior_running:
            maior_running = time()-init
        soma_running += time()-init
    
    print
    print('maior_update : %.4f sec' % (maior_update))
    print('maior_draw   : %.4f sec' % (maior_draw))
    print('maior_running: %.4f sec' % (maior_running))
    print
    print('media_update : %.4f sec' % (soma_update/quant))
    print('media_draw   : %.4f sec' % (soma_draw/quant))
    print('media_running: %.4f sec' % (soma_running/quant))
    pygame.quit()

def load():
    screen_size = (500, 500)
    surface = {
        'primeira'  : pygame.display.set_mode(screen_size),
        'screen'    : [],
    }
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('SHADERS TEST - ULISSES GANDINI')
    #pygame.mouse.set_visible(0)
    game_object = {
        'bg'            : [],
        'rect'          : [pygame.Rect(0, 0, 100, 100)]
    }
    var = {
        'folder'        : dirname(realpath(__file__)),
        'exit_request'  : False,
        'init_time'     : time()
    }


    game_object['bg'].append(Sprite(0, 0, var['folder']+'/bg.png'))
    game_object['bg'][0].img = pygame.transform.scale(game_object['bg'][0].img, screen_size)


    screen.blit(game_object['bg'][0].img, (game_object['bg'][0].x, game_object['bg'][0].y))
    for rect in game_object['rect']:
        pygame.draw.rect(surface['primeira'], (0, 0, 0), (rect.x, rect.y, rect.width, rect.height))
    pygame.display.flip()
    return True, {
        'screen_size'   : screen_size,
        'screen'        : screen,
        'game_object'   : game_object,
        'var'           : var,
        'surface'       : surface
    }

def update(settings):
    settings['game_object']['rect'][0].x += 1
    return settings

def draw(settings):
    game_object = settings['game_object']
    surface = settings['surface']
    for rect in game_object['rect']:
        pygame.draw.rect(surface['primeira'], (0, 0, 0), (rect.x, rect.y, rect.width, rect.height))
    fps(60)
    pygame.display.update(game_object['rect'])
    pass

def fps(frames):
    pygame.time.Clock().tick(frames)

class Cube2D():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

def joke(surface, time):
    for row in range(surface.get_height()):
        for column in range(surface.get_width()):
            if int(row+time)%20==0:
                surface.set_at((column, row), tuple([255-i for i in surface.get_at((column, row))]))
    return surface

def check_exit(settings):
    if settings['var']['exit_request']:
        return False
    k = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == QUIT or k[K_ESCAPE]:
            return False
    return True

class Sprite():
    def __init__(self, x, y, path, center=False):
        self.x = x
        self.y = y
        self.img = pygame.image.load(path)
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        if center:
            self.x = x-self.width/2
            self.y = y-self.height/2

main()