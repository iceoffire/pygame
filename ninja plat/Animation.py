import pygame
from time import time

class Animation()):
    def __init__(self, sprites, path):
        self.sprites     = sprites
        self.path        = path
        self.tile        = 'idle'
        self.pos         = 0
        self.last_update = time()
        self.img         = pygame.image.load(path + '/' + sprites[0][0] + '.png')

    def change(self, tile, num):
        self.tile        = tile
        self.img         = pygame.image.load(self.path + '/' + tile + num + '.png')

    def update(self):
        if time()-self.last_update>self.sprites[self.tile[1]]:
            if self.pos == self.sprites[self.tile]-1:
                self.pos     = 0
            else:
                self.pos    += 1
            self.img         = pygame.image.load(self.path + '/' + self.tile + self.pos + '.png')
            self.last_update = time()
