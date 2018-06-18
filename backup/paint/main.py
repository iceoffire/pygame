import pygame
from pygame.locals import *

def main():
    running, settings = load()
    reset_screen(settings)
    while running:
        settings = update(settings)
        draw(settings)
        running = check_exit(settings)
    pygame.quit()

def load():
    screen_size = (400, 400)
    screen = pygame.display.set_mode(screen_size)
    hud = pygame.display.set_mode(screen_size)
    circle = []
    var = {
        'exit_request'  : False
    }
    return True, {
        'screen_size'   : screen_size,
        'screen'        : screen,
        'hud'           : hud,
        'color'         : (150, 200, 150),
        'circle'        : circle,
        'var'           : var
    }

def update(settings):
    m = pygame.mouse.get_pressed()
    m_pos = pygame.mouse.get_pos()
    k = pygame.key.get_pressed()
    if k[K_x]:
        reset_screen(settings)

    if m[0]:
        pygame.draw.circle(settings['screen'], settings['color'], (m_pos[0], m_pos[1]), 4)
    return settings

def reset_screen(settings):
    screen  = settings['screen']
    hud     = settings['hud']
    screen.fill((255, 255, 255))
    for i in range(320):
        r = 255-(255*i/320)
        g = 0
        b = 0
        for j in range(10, 19):
            hud.set_at((j, i+40), (r, g, b, 255))
        r = 0
        g = 255-(255*i/320)
        b = 0
        for j in range(10, 19):
            hud.set_at((j+20, i+40), (r, g, b, 255))
        r = 0
        g = 0
        b = 255-(255*i/320)
        for j in range(10, 19):
            hud.set_at((j+40, i+40), (r, g, b, 255))
        
    pygame.draw.rect(hud, (0, 0, 0), (10, 40, 10, 320), 1)
    pygame.draw.rect(hud, (0, 0, 0), (30, 40, 10, 320), 1)
    pygame.draw.rect(hud, (0, 0, 0), (50, 40, 10, 320), 1)

def draw(settings):
    pygame.display.flip()
    pass

def check_exit(settings):
    if settings['var']['exit_request']:
        return False
    k = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == QUIT or k[K_ESCAPE]:
            return False
    return True

main()