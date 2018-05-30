import pygame
from pygame.locals import *
from os.path import dirname, realpath
from random import randint
from math import sin, cos, radians

def main():
    running, settings = load()
    while running:
        settings = update(settings)
        draw(settings)
        running = check_exit(settings)
    pygame.quit()

def load():
    screen_size = (380, 460)
    screen = pygame.display.set_mode(screen_size)
    pygame.font.init()
    game_object = {
        'posto'     : [],
        'list'      : [],
        'HUD'       : [],
        'bandeira'  : [],
        'nota'      : [],
    }
    var = {
        'folder'        : dirname(realpath(__file__)),
        'exit_request'  : False,
        'valor_nota'    : 1,
        'idle_gain'     : 0,
        'money'         : 0
    }
    game_object['bandeira'].append(Sprite((76, 40), var['folder']+'/assets/bandeira.png', 228, 160))
    return True, {
        'screen_size' : screen_size,
        'screen'        : screen,
        'game_object'   : game_object,
        'var'           : var
    }

def update(settings):
    m = pygame.mouse.get_pressed()[0]
    k = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == QUIT or k[K_ESCAPE]:
            settings['var']['exit_request'] = True 
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            pos = pygame.mouse.get_pos()
            if verificar_click(settings['game_object']['bandeira'][0], pos):
                pos = (pos[0]-36, pos[1]-15)
                settings['game_object']['nota'].append(Sprite(pos, settings['var']['folder'] + '/assets/notas/nota' + str(settings['var']['valor_nota'])+'.png', 68, 30))
                settings['var']['money'] += settings['var']['valor_nota']
    for gO in settings['game_object']['nota']:
        gO.y_speed += 0.5
        gO.y += gO.y_speed
        gO.rotation += gO.rotate_frame
        if gO.y > settings['screen_size'][1]:
            settings['game_object']['nota'].remove(gO)
    return settings

def draw(settings):
    screen_size = settings['screen_size']
    screen      = settings['screen']
    game_object = settings['game_object']
    font = pygame.font.SysFont("PressStart2P", 20)
    screen.fill((180, 200, 150))
    for name in ['bandeira', 'nota']:
        for gO in game_object[name]:
            if gO.__class__==Sprite:
                temp_img = pygame.transform.rotate(gO.img, gO.rotation)
                screen.blit(temp_img, (gO.x, gO.y))
    screen.blit(font.render(str(settings['var']['money']), True, (255, 255, 255)), (180-10*(len(str(settings['var']['money']))-1), 220))
    pygame.display.flip()
    fps(60)
    pass

def check_exit(settings):
    if settings['var']['exit_request']:
        return False
    else:
        return True

def fps(frames):
    pygame.time.Clock().tick(frames)

def verificar_click(box, pos):
    if box.__class__ == Sprite:
        if pos[0] >box.x and pos[0] < box.x+box.width and \
            pos[1]>box.y and pos[1] < box.y+box.height:
            return True
    return False

class Sprite():
    def __init__(self, (x, y), path, scale_x=None, scale_y=None):
        self.x = x
        self.y = y
        self.y_speed = 0
        self.img = pygame.image.load(path)
        self.rotation = 0
        self.rotate_frame = randint(-3, 3)
        if scale_x != None:
            self.img = pygame.transform.scale(self.img, (scale_x, scale_y))
        self.width = self.img.get_width()
        self.height = self.img.get_height()

main()