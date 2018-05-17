import pygame

class Collider2D_AABB():
    def __init__(self, obj, (x, y), width, height):
        self.x = x
        self.y = y
        self.obj = obj
        self.width = width
        self.height = height
    
    def update_move(self, game_object):
        if self.obj.x_speed <0:
            if not colliding_left(self.obj, game_object):
                self.obj.x += self.obj.x_speed
        else:
            if not colliding_right(self.obj, game_object):
                self.obj.x += self.obj.x_speed

        self.obj.y_speed += 1
        if not colliding_bottom(self.obj, game_object):
            self.obj.y += self.obj.y_speed
        self.x = self.obj.x
        self.y = self.obj.y
        

def colliding_left(obj, gO):
    return False #check colliders left_side

def colliding_right(obj, gO):
    return False #check colliders right_side

def colliding_bottom(obj, gO):
    return False