import pygame
from pygame.locals import *

def main():
    saida, settings = load()
    while not saida:
        settings = update(settings)
        draw(settings)
        saida = check_exit()
    pygame.quit()

def load():
    screen_size = (400, 400)
    screen = pygame.display.set_mode(screen_size)
    retangulo = pygame.Rect(150, 150, 100  , 100)
    #                      (x  , y,   width, height)
    return False, {
        'screen_size'   : screen_size,
        'screen'        : screen,
        'retangulo'     : retangulo
    }

def update(settings):
    k = pygame.key.get_pressed()
    screen_size = settings['screen_size']
    retangulo = settings['retangulo']
    if k[K_d] or k[K_RIGHT]:
        retangulo.x += 1
    elif k[K_a] or k[K_LEFT]:
        retangulo.x -= 1
    if k[K_w] or k[K_UP]:
        retangulo.y -= 1
    elif k[K_s] or k[K_DOWN]:
        retangulo.y += 1
    
    if retangulo.x <0:
        retangulo.x = 0
    if retangulo.y <0:
        retangulo.y = 0
    #screen_size[0] = width
    #screen_size[1] = height
    if retangulo.x+retangulo.width>screen_size[0]:
        retangulo.x = screen_size[0]-retangulo.width
    
    if retangulo.y+retangulo.height>screen_size[1]:
        retangulo.y = screen_size[1]-retangulo.height
    return settings

def draw(settings):
    screen = settings['screen']
    retangulo = settings['retangulo']
    cor_preta = (0, 0, 0)
    cor_branca =(255, 255, 255)
    screen.fill(cor_preta)
    #pygame.draw.rect(tela, cor, (x, y, width, hight), linha)
    pygame.draw.rect(screen, cor_branca, (retangulo.x, retangulo.y, retangulo.width, retangulo.height))
    pygame.display.flip()
    pygame.time.Clock().tick(300)


def check_exit():
    k = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == QUIT or k[K_ESCAPE]:
            return True
    return False

main()