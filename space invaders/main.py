import pygame, os
from pygame.locals import *
from time import time

def main():
    #Debug Var
    init = time()
    maior_update = 0
    maior_draw = 0
    maior_running = 0
    soma_update = 0
    soma_draw = 0
    soma_running = 0
    quant = 0
    
    running, settings = load()
    
    #debug
    print('load: ' + str(time()-init))
    init = time()
    while running:

        quant+=1
        init = time()

        settings = update(settings)

        if time()-init>maior_update:
            maior_update = time()-init
        soma_update += time()-init
        init = time()

        draw(settings)

        if time()-init>maior_draw:
            maior_draw = time()-init
        soma_draw += time()-init
        init = time()

        running = check_exit()
        if time()-init>maior_running:
            maior_running = time()-init
        soma_running += time()-init
    print
    print('maior_update  : %.4f sec' % (maior_update))
    print('maior_draw    : %.4f sec' % (maior_draw))
    print('maior_running : %.4f sec' % (maior_running))
    print
    print('media_update  : %.4f sec' % (soma_update/quant))
    print('media_draw    : %.4f sec' % (soma_draw/quant))
    print('media_running : %.4f sec' % (soma_running/quant))
    pygame.quit()

def load():
    screen_size = (400, 300)
    screen = pygame.display.set_mode(screen_size)
    game_object = {
        'player'     : [],
        'enemy'      : [],
        'bullet'     : [],
        'HUD'        : [],
        'kill_effect': []
    }
    var = {
        'folder'     : os.path.dirname(os.path.realpath(__file__)),
        'side'       : 1,
        'init'       : time(),
        'time_update': 0.3,
        'last_shoot' : time(),
    }
    game_object = load_level(1, game_object, var['folder'], screen_size)
    return True, {
        'screen_size'   : screen_size,
        'screen'        : screen,
        'game_object'   : game_object,
        'var'           : var
    }

def reset_game_object():
    game_object = {
        'player'     : [],
        'enemy'      : [],
        'bullet'     : [],
        'HUD'        : [],
        'kill_effect': []
    }
    return game_object

def load_level(level, game_object, folder, screen_size):
    game_object = reset_game_object()
    if level == 1:
        for linha in range(5):
            for coluna in range(12):
                x = 10+(screen_size[0]-10)/12*coluna
                y = 30+30*linha
                if linha == 0:
                    path = folder + '/assets/img/enemy2.png'
                    game_object['enemy'].append(Sprite(x, y, path, 2))
                elif linha == 1 or linha == 2:
                    path = folder + '/assets/img/enemy3.0.png'
                    game_object['enemy'].append(Sprite(x, y, path, 2, [{'enemy3.' : 2}, 'enemy3.']))
                else:
                    path = folder + '/assets/img/enemy1.png'
                    game_object['enemy'].append(Sprite(x, y, path, 2))
        game_object['player'].append(Sprite(screen_size[0]/2-15, screen_size[1]*0.88, folder + '/assets/img/player.png', 2))
    else:
        win()
    return game_object

def win():
    pass

def update(settings):
    game_object = settings['game_object']
    k = pygame.key.get_pressed()
    for name in game_object:
        for gO in game_object[name]:
            if gO.x<=0:
                settings['var']['side'] = 1
            if gO.x+gO.width >= settings['screen_size'][0]:
                settings['var']['side'] = -1
    if time() - settings['var']['init'] > settings['var']['time_update']:
        for gO in game_object['enemy']:
            gO.x += settings['var']['side']
            if gO.animation != None:
                gO.animation.update()
        settings['var']['init'] = time()
    player = game_object['player'][0]
    if k[K_d] or k[K_RIGHT]:
        player.x += 6
    elif k[K_a] or k[K_LEFT]:
        player.x -= 6
    
    if player.x <0:
        player.x = 0
    if player.x+player.width > settings['screen_size'][0]:
        player.x = settings['screen_size'][0]-player.width

    if k[K_SPACE]:
        if time()-settings['var']['last_shoot'] > 0.24:
            game_object = shoot(game_object, player)
            settings['var']['last_shoot'] = time()

    for bullet in game_object['bullet']:
        bullet.y -= 2
        if bullet.y+bullet.height < 0:
            game_object['bullet'].remove(bullet)

    for kill_effect in game_object['kill_effect']:
        if time()-kill_effect.init > 0.2:
            game_object['kill_effect'].remove(kill_effect)

    game_object =  verificar_colisao(game_object, settings['var']['folder'])
    return settings

def shoot(game_object, origem):
    game_object['bullet'].append(Box2D(origem.x+origem.width/2-1, origem.y-10, 2, 10, (255, 255, 255)))
    return game_object

def verificar_colisao(game_object, folder):
    for bullet in game_object['bullet']:
        for gO in game_object['enemy']:
            if (bullet.x > gO.x and bullet.x < gO.x+gO.width) or \
                (bullet.x+bullet.width > gO.x and bullet.x+bullet.width < gO.x+gO.width):
                if bullet.y<gO.y and bullet.y+bullet.height>gO.y:
                    game_object['kill_effect'].append(Sprite(gO.x, gO.y, folder + '/assets/img/kill_effect.png', 2))
                    game_object['bullet'].remove(bullet)
                    game_object['enemy'].remove(gO)
                    break
    return game_object

def draw(settings):
    game_object = settings['game_object']
    screen = settings['screen']
    screen.fill((0, 0, 0))
    for name in game_object:
        for gO in game_object[name]:
            if gO.__class__ == Sprite:
                temp_img = pygame.transform.scale(gO.img, (gO.width, gO.height))
                screen.blit(temp_img, (gO.x, gO.y))
            elif gO.__class__ == Box2D:
                pygame.draw.rect(screen, gO.color, (gO.x, gO.y, gO.width, gO.height))
    pygame.display.flip()
    fps(60)
    pass

def fps(frames):
    pygame.time.Clock().tick(frames)

def check_exit():
    k = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == QUIT or k[K_ESCAPE]:
            return False
    return True

class Sprite():
    def __init__(self, x, y, path, scale=1, animation=None):
        self.x = x
        self.y = y
        self.scale = scale
        self.init = time()
        self.img = pygame.image.load(path)
        self.width = self.img.get_width()*scale
        self.height= self.img.get_height()*scale
        if animation != None:
            self.animation = Animation(animation[0], os.path.dirname(path), animation[1], self)
        else:
            self.animation = None

class Animation():
    def __init__(self, sprite, path, first, obj):
        self.sprite = sprite
        self.path = path
        self.actual = first
        self.obj = obj
        self.num = 0
    def update(self):
        self.num += 1
        if self.num > self.sprite[self.actual]-1:
            self.num = 0
        self.obj.img = pygame.image.load(self.path + '/' + self.actual + str(self.num) + '.png')
    def change(self, what_to):
        self.actual = what_to
        self.num = 0
        self.obj.img = pygame.image.load(self.path + '/' + self.actual + str(self.num) + '.png')

class Box2D():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.y_speed = 0

main()