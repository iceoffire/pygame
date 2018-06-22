import pygame
from pygame.locals import *
from random import randint

from pygame import gfxdraw

def main():
    running, settings = load()
    while running:
        settings = update(settings)
        draw(**settings)
        running = check_exit(**settings)
    pygame.quit()
    quit()

def load():
    screen_size = (800,600)
    screen = pygame.display.set_mode(screen_size)
    forms = {
        'circle'    : [Circle(30, 40, 20), Circle(300, 40, 2)],#aqui vamos usar uma lista mas vamos criar formas aa (antialiasing)
        'rect'      : [Rect(60, 40, 40,40)],
        'line'      : [Line((10,10) ,(30,10))],
        'polygon'   : [Polygon(((400, 400), (300, 500), (200, 400)))],
        'ellipse'   : [Ellipse(200, 100, 20, 40)],
        'surface'   : [Surface(500, 400, pygame.Surface((300, 300)).convert_alpha())],
    }
    return True, {
        'screen_size'   : screen_size,
        'screen'        : screen,
        'forms'         : forms,
        'exit_request'  : False,
    }

def update(settings):
    for e in pygame.event.get():
        if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
            settings['exit_request'] = True
    return settings

def draw(screen_size, screen, forms, **kwargs):
    screen.fill((40,40,40))
    for name in forms:
        
        for gO in forms[name]:
            if gO.__class__==Circle:
                pygame.gfxdraw.aacircle(screen, gO.x,gO.y, gO.r, gO.color)
                pygame.gfxdraw.filled_circle(screen, gO.x,gO.y, gO.r, gO.color)
            elif gO.__class__==Rect:
                pygame.draw.rect(screen, gO.color, (gO.x, gO.y, gO.w, gO.h))
            elif gO.__class__==Line:
                pygame.draw.aaline(screen, gO.color, gO.start_pos, gO.end_pos)
            elif gO.__class__==Polygon:
                pygame.gfxdraw.aapolygon(screen, gO.point_list, gO.color)
                pygame.gfxdraw.filled_polygon(screen, gO.point_list, gO.color)
            elif gO.__class__==Ellipse:
                pygame.gfxdraw.aaellipse(screen, gO.x, gO.y, gO.rx, gO.ry, gO.color)
                pygame.gfxdraw.filled_ellipse(screen, gO.x, gO.y, gO.rx, gO.ry, gO.color)
            elif gO.__class__==Surface:
                screen.blit(gO.surf, (gO.x, gO.y))
    pygame.display.flip()
    pass

def check_exit(exit_request, **kwargs):
    return not exit_request

class Mov:
    x_speed = 0
    y_speed = 0

class Circle(Mov):
    color = (randint(0,255),randint(0,255),randint(0,255))
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
    

class Rect(Mov):
    color = (randint(0,255),randint(0,255),randint(0,255))
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

class Line(Mov):
    color = (randint(0,255),randint(0,255),randint(0,255))
    def __init__(self, start_pos, end_pos):
        self.start_pos = start_pos
        self.end_pos = end_pos

class Polygon(Mov):
    color = (randint(0,255),randint(0,255),randint(0,255))
    def __init__(self, point_list):
        self.point_list = point_list

class Ellipse(Mov):
    color = (randint(0,255),randint(0,255),randint(0,255))
    def __init__(self, x, y, rx, ry):
        self.x = x
        self.y = y
        self.rx = rx
        self.ry = ry

class Surface(Mov):
    def __init__(self, x, y, surf):
        self.x = x
        self.y = y
        self.surf = surf

if __name__=="__main__":
    main()
