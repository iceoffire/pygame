import pygame
from pygame.locals import *

class Collider2D_AABB():
    def __init__(self, obj, (x, y), width, height):
        self.x = x
        self.y = y
        self.obj = obj
        self.width = width
        self.height = height
    
    def update_move(self, game_object):
        k = pygame.key.get_pressed()
        if k[K_d]:
            self.obj.x_speed += 3
        elif k[K_a]:
            self.obj.x_speed -= 3
        else:
            self.obj.x_speed /= 2.2
            if abs(self.obj.x_speed) < 0.1:
                self.obj.x_speed = 0
        
        if k[K_SPACE] and self.obj.is_grounded:
            self.obj.y_speed = -20
            self.obj.is_grounded = False

        if abs(self.obj.x_speed) > 8:
            if self.obj.x_speed > 0:
                self.obj.x_speed = 8
            else:
                self.obj.x_speed = -8

        if self.obj.x_speed <0:
            if not colliding_left(self.obj, game_object):
                self.obj.x += self.obj.x_speed
        else:
            if not colliding_right(self.obj, game_object):
                self.obj.x += self.obj.x_speed

        self.obj.y_speed += 1
        if not colliding_bottom(self.obj, game_object):
            self.obj.y += self.obj.y_speed
        else:
            if self.obj.y_speed>0:
                self.obj.y_speed = 0
                self.obj.is_grounded = True
        if colliding_top(self.obj, game_object):
            self.obj.y_speed = 0
            self.obj.y += 1
        self.x = self.obj.x
        self.y = self.obj.y
        

def colliding_top(obj, game_object):
    for name in game_object:
        for gO in game_object[name]:
            if obj != gO:
                if obj.y<gO.y+gO.height and obj.y+obj.height>gO.y+gO.height:
                    if (obj.x>gO.x and obj.x<gO.x+gO.width) or (obj.x+obj.width>gO.x and obj.x+obj.width<gO.x+gO.width):
                        if obj.y-gO.y+gO.height<10:
                            obj.y = gO.y+gO.height
                        return True
    return False


def colliding_left(obj, game_object):
    for name in game_object:
        for gO in game_object[name]:
            if obj != gO:
                if obj.x+obj.x_speed<gO.x+gO.width and obj.x+obj.width>gO.x+gO.width:
                    if (obj.y> gO.y and obj.y < gO.y+gO.height) or \
                       (obj.y+obj.height > gO.y and obj.y+obj.height < gO.y + gO.height) or \
                       (obj.y<=gO.y and obj.y+obj.height>gO.y+gO.height):
                        return True
    return False #check colliders left_side

def colliding_right(obj, game_object):
    for name in game_object:
        for gO in game_object[name]:
            if obj != gO:
                if obj.x+obj.width>gO.x and obj.x<gO.x:
                    if (obj.y> gO.y and obj.y < gO.y+gO.height) or \
                       (obj.y+obj.height > gO.y and obj.y+obj.height < gO.y + gO.height) or \
                       (obj.y<=gO.y and obj.y+obj.height>gO.y+gO.height):
                       return True
    return False #check colliders right_side

def colliding_bottom(obj, game_object):
    for name in game_object:
        for gO in game_object[name]:
            if obj != gO:
                if obj.y+obj.height+obj.y_speed>gO.y and obj.y+obj.height+obj.y_speed<gO.y+gO.height:
                    if (obj.x>gO.x and obj.x<gO.x+gO.width) or (obj.x+obj.width>gO.x and obj.x+obj.width<gO.x+gO.width):
                        if gO.y-obj.y+obj.height<5:
                            print('oi')
                            obj.y = gO.y-obj.height
                        return True
    return False