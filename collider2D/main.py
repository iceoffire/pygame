import pygame
from pygame.locals import *

def main():
    running = load()
    while running:
        update()
        draw()
        running = check_exit()
    pygame.quit()

def load():
    load_vars()
    return True

def load_vars():
    global screen_size, screen, game_object, layers, cam
    screen_size = (400, 400)
    screen = pygame.display.set_mode(screen_size)
    game_object = {
        'player' : [],
        'objects': []
    }
    layers = ['objects', 'player']
    cam = Camera((0, 0), 1)

def update():
    pass

def draw():
    camera()
    pass

def camera():
    for name in layers:
        for gO in game_object[name]:
            x = cam.x + gO.x * cam.scale
            pygame.draw.rect()

class Camera():
    def __init__(self, (x, y), scale):
        self.x, self.y = x, y
        self.scale = scale