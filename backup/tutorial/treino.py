import pygame
from pygame.locals import *

def main():
    running, settings = load()
    while running:
        settings = update(settings)
        draw(settings)
        running = check_exit()
    pygame.quit()

def load():
    retangulo = pygame.Rect(170, 170, 60, 60)
    screen_size = (400, 400)
    screen = pygame.display.set_mode(screen_size)
    return True, {
        'screen_size' : screen_size,
        'screen'      : screen,
        'retangulo'   : retangulo
    }

def update(settings):
    return settings

def draw(settings):
    screen = settings['screen']
    rect = settings['retangulo']
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (255, 255, 0), (200, 200), 30)
    pygame.draw.rect(screen, (255, 0, 0), (rect.x, rect.y, rect.width, rect.height), 1)
    pygame.display.flip()

def check_exit():
    k = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == QUIT or k[K_ESCAPE]:
            return False
    return True

main()