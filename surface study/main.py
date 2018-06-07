import pygame
from pygame.locals import *
from os.path import dirname, realpath

def main():
    running, settings = load()
    while running:
        settings = update(settings)
        draw(**settings)
        running = check_exit(**settings)
    pygame.quit()

def load():
    screen_size = (640, 500)
    screen = pygame.display.set_mode(screen_size)
    exit_request = False
    var = {
        'folder' : dirname(realpath(__file__))
    }

    my_surface = load_level(1)
    my_surface = pygame.transform.scale(my_surface, screen_size)
    return True, {
        'screen_size'   : screen_size,
        'screen'        : screen,
        'my_surface'    : my_surface,
        'exit_request'  : exit_request,
        'x'             : 0,
    }

def load_level(level):
    image = pygame.image.load(dirname(realpath(__file__))+'/img/map/map'+str(level)+'.png')
    width = image.get_width()
    height =image.get_height()
    my_surface = pygame.Surface((width*128, height*128))
    for row in range(height):
        for column in range(width):
            x = column*128
            y = row*128
            color = str(image.get_at((column, row)))
            obj_img = get_object(color)
            if obj_img != False:
                my_surface.blit(pygame.image.load(dirname(realpath(__file__))+obj_img),(x, y))
    return my_surface

def get_object(color):# -> Surface
    obj_mem = {
        '(0, 0, 0, 255)' : '/img/tile/FMF.png'
    }
    if color in obj_mem:
        return obj_mem[color]
    else:
        return False


def update(settings):
#    settings['x'] -=1
    for e in pygame.event.get():
        if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
            settings['exit_request'] = True
    return settings

def draw(screen_size, screen, my_surface, x, **kwargs):
    screen.fill((0, 0, 0))
    #temp_img = pygame.transform.scale(my_surface, screen_size)
    screen.blit(my_surface, (x, 0))
    pygame.display.flip()
#    fps(60)
    pass

def fps(frame):
    pygame.time.Clock().tick(frame)

def check_exit(exit_request, **kwargs):
    return not exit_request

main()
