import pygame
from pygame.locals import *
from random import randint

def main():
    running, settings = load()
    while running:
        settings = update(settings)
        draw((settings['game_object'], settings['camera'], settings['screen'], settings['screen_size'], settings['layers']))
        running = check_exit()
    pygame.quit()

def load():
    screen_size = (400, 400)
    screen = pygame.display.set_mode(screen_size)
    game_object = {
        'player' : [Box2D(40, 30, 30, 30, 1)],
        'objects': []
    }
    for i in range(30):
        game_object['objects'].append(Box2D(30*i, 340, 30, 30, 0))
    for j in range(2):
        for i in range(10):
            game_object['objects'].append(Box2D((30*29)*j, 340-30*i, 30, 30, 0))
    camera = Camera((0, 0), 1)
    return True, { #dict with my vars
            'game_object' : game_object,
            'screen_size'  : screen_size,
            'screen'       : screen,
            'camera'       : camera,
            'layers'       : ['objects', 'player'],
    }

def update(settings):
    settings['game_object'] = move(settings['game_object'])
    return settings

def draw(settings):
    reset_screen(settings[2])      #settings[2] == screen
    draw_on_camera(settings)    #settings = {'game_objects', 'screen_size', 'screen', 'camera', 'layers'}
    display_screen()               #settings[2] == screen
    fps(60)

def fps(frames):
    pygame.time.Clock().tick(frames)

def reset_screen(screen):
    screen.fill((0, 0, 0))

def display_screen():
    pygame.display.flip()

def draw_on_camera(settings):
    game_object = settings[0]
    camera = settings[1]
    screen = settings[2]
    screen_size = settings[3]
    layers = settings[4]
    for name in layers:
        for gO in game_object[name]:
            if gO.__class__ == Box2D:
                pygame.draw.rect(screen, gO.color, (gO.x, gO.y, gO.width, gO.height))

def check_exit():
    k = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == QUIT or k[K_ESCAPE]:
            return False
    return True

class Camera():
    def __init__(self, (x, y), scale):
        self.x = x
        self.y = y
        self.bounds = (0, 0)
        self.scale = scale
    def set_focus((x, y)):
        self.x = x #deixar fluido
        self.y = y
    def setScale(self, new_scale):
        self.scale = new_scale
        #self.bounds = calcularBounds() 


class Box2D():
    def __init__(self, x, y, width, height, gravity):
        self.x       = x
        self.y       = y
        self.x_speed = 0
        self.y_speed = 0
        self.width   = width
        self.height  = height
        self.color   = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.gravity = gravity

def move(game_object):
    game_object = gravity(game_object)
    move_space(game_object)
    return game_object

def gravity(game_object):
    for name in game_object:
        for gO in game_object[name]:
            if gO.gravity:
                gO.y_speed += 1
    return game_object

def move_space(game_object):
    for name in game_object:
        for gO in game_object[name]:
            collider = Collider(gO, game_object)
            print(collider)
            if collider['left'] or collider['right']:
                gO.x_speed = 0
            if collider['bottom']:
                gO.y_speed = 0
            
            gO.x += gO.x_speed
            gO.y += gO.y_speed

def Collider(gO, game_object):
    left   = check_left    (gO, game_object)
    right  = check_right   (gO, game_object)
    top    = check_top     (gO, game_object)
    bottom = check_bottom  (gO, game_object)
    return {
        'left'   : left,
        'right'  : right,
        'top'    : top, 
        'bottom' : bottom
    }

def check_left(obj, game_object):
    return False
def check_right(obj, game_object):
    return False
def check_top(obj, game_object):
    return False
def check_bottom(obj, game_object):
    for name in game_object:
        for gO in game_object[name]:
            if gO != obj:
                if (obj.y+obj.height+obj.y_speed>gO.y) and (obj.y+obj.height<gO.y+gO.height):
                    if (obj.x>=gO.x and obj.x<=gO.x+gO.width) or (obj.x+obj.width>=gO.x and obj.x+obj.width<=gO.x+gO.width):
                        return True
    return False

if __name__=='__main__':
    main()