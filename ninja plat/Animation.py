import pygame
from time import time

class Animation():
    def __init__(self, sprites, path, first):
        self.sprites     = sprites
        self.path        = path
        self.tile        = first
        self.pos         = 0
        self.last_update = time()
        self.img         = pygame.image.load(path + '/' + first + str(self.pos) + '.png')

    def change(self, tile, pos=0):
        self.tile        = tile
        self.img         = pygame.image.load(self.path + '/' + tile + pos + '.png')

    def update(self):
        if time()-self.last_update>self.sprites[self.tile[1]]:
            if self.pos == self.sprites[self.tile]-1:
                self.pos     = 0
            else:
                self.pos    += 1
            self.img         = pygame.image.load(self.path + '/' + self.tile + self.pos + '.png')
            self.last_update = time()
