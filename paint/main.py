import pygame
from pygame.locals import *

def main():
    running, settings = load()
    while running:
        settings = update(settings)
        draw(settings)
        running = check_exit(settings)
    pygame.quit()

def load():
    screen_size = (400, 400)
    screen = pygame.display.set_mode(screen_size)
    screen.fill((255, 255, 255))
    circle = []
    var = {
        'exit_request'  : False
    }
    return True, {
        'screen_size'   : screen_size,
        'screen'        : screen,
        'circle'        : circle,
        'var'           : var
    }

def update(settings):
    m = pygame.mouse.get_pressed()
    m_pos = pygame.mouse.get_pos()
    if m[0]:
        pygame.draw.circle(settings['screen'], (0, 0, 0), (m_pos[0], m_pos[1]), 4)
    return settings

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