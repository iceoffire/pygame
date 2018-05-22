import pygame, os
from pygame.locals import *

def main():
    running, settings = load()
    while running:
        settings = update(settings)
        draw(settings)
        running = check_exit(settings)
    pygame.quit()

def load():
    screen_size = (300, 300)
    screen = pygame.display.set_mode(screen_size)
    pygame.font.init()
    game_object = {
        'player1'   : [Box2D(0, 105, 10, 90, (255, 0, 0))],
        'player2'   : [Box2D(290, 105, 10, 90, (0, 0, 255))],
        'ball'      : [],
    }
    return True, {
        'screen_size'   : screen_size,
        'screen'        : screen,
        'game_object'   : game_object,
        'stop_running'  : False,
        'font'          : pygame.font.SysFont("arial", 20),
    }

def update(settings):
    game_object = settings['game_object']
    screen_size = settings['screen_size']
    k = pygame.key.get_pressed()
    player1 = game_object['player1'][0]
    player2 = game_object['player2'][0]
    if k[K_w]:
        player1.y -= 8
    elif k[K_s]:
        player1.y += 8

    if k[K_UP]:
        player2.y -= 8
    elif k[K_DOWN]:
        player2.y += 8

    if player1.y<0:
        player1.y = 0
    if player2.y<0:
        player2.y = 0

    if player1.y+player1.height>screen_size[1]:
        player1.y = screen_size[1] - player1.height
    if player2.y+player2.height>screen_size[1]:
        player2.y = screen_size[1] - player2.height
    return settings

def draw(settings):
    game_object = settings['game_object']
    screen      = settings['screen']
    screen_size = settings['screen_size']
    font = settings['font']
    screen.fill((0, 0, 0))
    drawHUD(screen, screen_size, font)
    for name in game_object:
        for gO in game_object[name]:
            if gO.__class__==Box2D:
                pygame.draw.rect(screen, gO.color, (gO.x, gO.y, gO.width, gO.height))
    pygame.display.flip()
    fps(60)
    pass

def fps(frames):
    pygame.time.Clock().tick(frames)

def drawHUD(screen, screen_size, font):
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, screen_size[0], screen_size[1]), 1)
    pygame.draw.line(screen, (255, 255, 255), (screen_size[0]/2, 0), (screen_size[0]/2, screen_size[1]), 1)
    pygame.draw.rect(screen, (0, 0, 0), (screen_size[0]*0.35, 0, screen_size[0]*0.3, screen_size[0]*0.2))
    pygame.draw.rect(screen, (255, 255, 255), (screen_size[0]*0.35, 0, screen_size[0]*0.3, screen_size[0]*0.2), 1)

def check_exit(settings):
    if settings['stop_running']:
        return False
    k = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == QUIT or k[K_ESCAPE]:
            return False
    return True

class Box2D():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

main()