import pygame
from pygame.locals import *
from os.path import realpath, dirname
from time import time
from random import randint


def main():
    running, settings = load()
    while running:
        settings = update(settings)
        draw(**settings)
        running = check_exit(**settings)
    pygame.quit()
    quit()


def load():
    screen_size = (450, 333)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Shoot'n up")
    game_object = {
        'player': Player(),
        'enemy': [],
        'shoot': [],
        'jump_scare': [],
        'hit_effect': [],
        'shoot_effect': [],
        'bg': Background(),
        'HUD': [Sprite(dirname(realpath(__file__))+'/assets/img/effects/HUD_Vidas.png', 20, 300)],
    }
    game_object = load_level(game_object, 1)
    path = dirname(realpath(__file__))
    last_shoot = time()
    level = 1
    return True, {
        'screen_size': screen_size,
        'screen': screen,
        'game_object': game_object,
        'path': path,
        'exit_request': False,
        'last_shoot': last_shoot,
        'level': level,
        'enemy_last_shoot': time()
    }


def load_level(game_object, what_level):
    path = dirname(realpath(__file__))
    if what_level == 1:
        for j in range(10):
            if j % 2:
                game_object['enemy'].append(Enemy(20+40*j, 40, 0, 0.5))
            else:
                game_object['enemy'].append(Enemy(20+40*j, 40, 0, 1))
    elif what_level == 2:
        for i in range(3):
            for j in range(10):
                game_object['enemy'].append(Enemy(20+40*j, -70-80*i, i, .8))
    elif what_level == 3:
        for i in range(5):
            if i % 2:
                for j in range(5):
                    x = 20+(440/5*j)
                    game_object['enemy'].append(Enemy(x, -70-80*i, i % 3, .8))
            else:
                for j in range(10):
                    x = 20+(440/10*j)
                    game_object['enemy'].append(Enemy(x, -70-80*i, i % 3, .8))
    else:
        for i in range(randint(2, 8)):
            foo = randint(5, 10)
            for j in range(foo):
                x = 20+(440/foo*j)
                if (i == 1 or i == 5) and j % 2:
                    game_object['enemy'].append(Enemy(x, -70-80*i, i % 3, 2))
                else:
                    game_object['enemy'].append(Enemy(x, -70-80*i, i % 3, 1))
    return game_object


def update(settings):
    settings = check_keys(settings)
    if len(settings['game_object']['enemy']) == 0:
        settings['level'] += 1
        load_level(settings['game_object'], settings['level'])

    settings['game_object']['player'].load_img()
    settings['game_object']['shoot'] = update_shoot(
        settings['game_object']['shoot'])
    settings['game_object']['bg'].tile, settings['game_object']['bg'].time = update_bg(
        settings['game_object']['bg'].tile, settings['game_object']['bg'].time)
    settings['game_object']['bg'] = parallax(
        settings['game_object']['player'], settings['game_object']['bg'])
    settings['game_object']['enemy'] = update_enemy(
        settings['game_object']['enemy'], settings['screen_size'], settings)
    settings['game_object'] = collider(settings['game_object'])
    for fire in settings['game_object']['player'].fires:
        fire.animation.update()
    for gO in settings['game_object']['enemy']:
        gO.fire.animation.update()
    for explosion in settings['game_object']['hit_effect']:
        explosion.animation.update()
        if explosion.animation.pos == 7:
            settings['game_object']['hit_effect'].remove(explosion)
    for gO in settings['game_object']['shoot_effect']:
        gO.animation.update()
        gO.x += settings['game_object']['player'].x_speed
        if gO.animation.pos == 6:
            settings['game_object']['shoot_effect'].remove(gO)
    return settings


def collider(game_object):
    for shoot in game_object['shoot']:
        if shoot.origin == 'player':
            for enemy in game_object['enemy']:
                if (shoot.x > enemy.x and shoot.x < enemy.x+enemy.width) or \
                        (shoot.x+shoot.width > enemy.x and shoot.x+shoot.width < enemy.x+enemy.width):
                    if (shoot.y < enemy.y+enemy.height and shoot.y > enemy.y):
                        x, y = shoot.x-53/2, shoot.y-25
                        game_object['hit_effect'].append(Hit_effect(x, y))
                        enemy.hit_demage()
                        game_object['shoot'].remove(shoot)
                        if enemy.hp <= 0:
                            game_object['enemy'].remove(enemy)
                        break
            if shoot.y < 0:
                try:
                    game_object['shoot'].remove(shoot)
                except:
                    None
        if shoot.origin == 'enemy':
            player = game_object['player']
            if (shoot.x > player.x and shoot.x < player.x+player.width) or \
                    (shoot.x+shoot.width > player.x and shoot.x+shoot.width < player.x+player.width):
                if (shoot.y < player.y+player.height and shoot.y > player.y):
                    x, y = shoot.x-53/2, shoot.y-25
                    game_object['hit_effect'].append(Hit_effect(x, y))
                    game_object['shoot'].remove(shoot)
                    game_object['player'].hp -= 1
                    break
            if shoot.y < 0:
                try:
                    game_object['shoot'].remove(shoot)
                except:
                    None
    return game_object


def update_enemy(enemy, screen_size, settings):
    enemy_who_gonna_shoot = randint(0, len(enemy))
    index = 0
    for gO in enemy:
        if index == enemy_who_gonna_shoot and time()-settings['enemy_last_shoot'] > 0.5:
            x = gO.x+gO.width/2-8
            y = gO.y+gO.height
            settings['game_object']['shoot'].append(Shoot(x, y, 'enemy'))
            settings['game_object']['shoot_effect'].append(
                Shoot_effect(x, y, 'enemy'))
            settings['enemy_last_shoot'] = time()
        gO.y += gO.y_speed
        if time()-gO.init > 0.1 and gO.hit_mark:
            gO.image_return()
            gO.hit_mark = False
        if gO.y > screen_size[1]:
            enemy.remove(gO)
        index += 1
    return enemy


def parallax(player, bg):
    middle = player.x
    foo = -middle/225.00*25
    bg.x = foo
    return bg


def update_shoot(shoot):
    for gO in shoot:
        gO.y += gO.y_speed
    return shoot


def check_keys(settings):
    k = pygame.key.get_pressed()
    settings['game_object']['player'].player_move_key(
        k, settings['screen_size'])
    for e in pygame.event.get():
        if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
            settings['exit_request'] = True
    if k[K_SPACE] and time()-settings['last_shoot'] > 0.24:
        x, y = settings['game_object']['player'].x, settings['game_object']['player'].y
        settings['game_object']['shoot'].append(Shoot(x, y+3, 'player'))
        settings['game_object']['shoot'].append(Shoot(x+24, y+3, 'player'))
        settings['game_object']['shoot_effect'].append(
            Shoot_effect(x, y-14, 'player'))
        settings['game_object']['shoot_effect'].append(
            Shoot_effect(x+22, y-14, 'player'))
        settings['last_shoot'] = time()
    return settings


def update_bg(tile, last_time):
    if time()-last_time > 0.02:
        tile = (tile+1) % 200
        last_time = time()
    return tile, last_time


def draw(game_object, screen, screen_size, path, **kwargs):
    draw_bg(screen, game_object['bg'])
    draw_enemy(screen, game_object['enemy'])
    draw_shoot_effect(screen, game_object['shoot_effect'])
    draw_player(screen, game_object['player'])
    draw_HUD(screen, game_object['HUD'], game_object['player'].hp)
    draw_shoot(screen, game_object['shoot'])
    draw_hit_effect(screen, game_object['hit_effect'])
    pygame.display.flip()
    fps(60)
    pass


def draw_shoot_effect(screen, effect):
    for gO in effect:
        screen.blit(gO.img, (int(gO.x), int(gO.y)))


def draw_hit_effect(screen, explosion):
    for gO in explosion:
        screen.blit(gO.img, (int(gO.x), int(gO.y)))


def draw_shoot(screen, shoot):
    for gO in shoot:
        screen.blit(gO.img, (int(gO.x), int(gO.y)))


def draw_enemy(screen, enemy):
    for gO in enemy:
        screen.blit(gO.fire.img, (int(gO.x+16), int(gO.y-7)))
        screen.blit(gO.img, (int(gO.x), int(gO.y)))


def draw_HUD(screen, HUD, lifes):
    for gO in HUD:
        if gO.__class__ == Sprite:
            x = gO.x
            screen.blit(gO.img, (int(gO.x), int(gO.y)))
    img = pygame.image.load(dirname(realpath(__file__)) +
                            '/assets/img/effects/life.png')
    for i in range(lifes-1):
        screen.blit(img, (int(x+5+22*i), int(305)))


def draw_player(screen, player):
    screen.blit(player.img, (int(player.x), int(player.y)))
    y = player.fires[0].y+player.height-5
    if player.pos == 'M':
        x = player.x+2  # compensar o offset do primeiro fogo
        x_offset = 25  # compensar o offset do segundo fogo
    else:
        x = player.x+4  # compensar o offset do primeiro fogo
        x_offset = 18  # compensar o offset do segundo fogo
    screen.blit(player.fires[0].img, (int(x), int(y)))
    screen.blit(player.fires[0].img, (int(x+x_offset), int(y)))


def fps(frames):
    pygame.time.Clock().tick(frames)


def draw_bg(screen, bg):
    screen.blit(bg.img[bg.tile], (int(bg.x), int(bg.y)))
    pass


def check_exit(exit_request, **kwargs):
    return not exit_request


class Hit_effect:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        path = dirname(realpath(__file__))+'/assets/img/effects'
        self.img = pygame.image.load(path+'/explosion0.png')
        self.animation = Animation(
            {'explosion': [8, 0.01]}, path, 'explosion', self)


class Shoot_effect:
    def __init__(self, x, y, origin):
        self.x = x
        self.y = y
        self.origin = origin
        path = dirname(realpath(__file__))
        if origin == 'player':
            self.img = pygame.image.load(
                path+'/assets/img/effects/fire_effectPlayer0.png')
            self.animation = Animation({'fire_effectPlayer': [
                                       7, 0]}, path+'/assets/img/effects', 'fire_effectPlayer', self)
        else:
            self.img = pygame.image.load(
                path+'/assets/img/effects/fire_effectEnemy0.png')
            self.animation = Animation(
                {'fire_effectEnemy': [7, 0]}, path+'/assets/img/effects', 'fire_effectEnemy', self)


class Shoot:
    def __init__(self, x, y, origin):
        self.x = x
        self.y = y
        self.origin = origin
        if origin == 'player':
            self.img = pygame.image.load(
                dirname(realpath(__file__))+'/assets/img/effects/shootPlayer.png')
            self.y_speed = -4
        else:
            self.img = pygame.image.load(
                dirname(realpath(__file__))+'/assets/img/effects/shootEnemy.png')
            self.y_speed = 4
        self.width = self.img.get_width()
        self.height = self.img.get_height()


class Sprite:
    def __init__(self, path, x, y):
        self.x = x
        self.y = y
        self.img = pygame.image.load(path)


class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        path = dirname(realpath(__file__))
        self.img = pygame.image.load(path+'/assets/img/effects/explosion0.png')
        self.animation = Animation(
            {'explosion': [7, 0.2]}, path, 'explosion', self)


class Enemy:
    def __init__(self, x, y, type, y_speed):
        self.x = x
        self.x_speed = 0
        self.y = y
        self.hp = type+2
        self.y_speed = y_speed
        self.type = type
        self.img = pygame.image.load(dirname(
            realpath(__file__))+'/assets/img/enemy/enemy'+str(type)+'.png').convert_alpha()
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.fire = Fire(self)
        self.init = time()
        self.hit_mark = False

    def hit_demage(self):
        if randint(1, 2) % 2:
            self.img = white(self.img)
        else:
            self.img = red(self.img)
        self.hit_mark = True
        self.hp -= 1
        self.init = time()

    def image_return(self):
        self.img = pygame.image.load(dirname(realpath(
            __file__))+'/assets/img/enemy/enemy'+str(self.type)+'.png').convert_alpha()


def white(surface):
    for row in range(surface.get_height()):
        for column in range(surface.get_width()):
            if surface.get_at((column, row))[3] == 255:
                surface.set_at((column, row), (255, 255, 255))
    return surface


def red(surface):
    for row in range(surface.get_height()):
        for column in range(surface.get_width()):
            if surface.get_at((column, row))[3] == 255:
                surface.set_at((column, row), (255, 130, 130))
    return surface


class Player:
    def __init__(self):
        self.pos = 'M'
        self.hp = 4
        self.x = 200
        self.x_speed = 0
        self.y = 280
        self.tiles = {}
        self.spaw_effect = False
        self.spaw_effect_start = time()
        self.fires = [
            Fire(self),
            Fire(self)
        ]
        path = dirname(realpath(__file__))
        for sides in ['L', 'M', 'R']:
            for i in range(4):
                k = i+1
                self.tiles[str(k)+sides] = (pygame.image.load(path +
                                                              '/assets/img/ships/ship' + str(k) + sides + '.png'))
        self.load_img()
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def load_img(self):
        self.img = self.tiles[str(self.hp)+self.pos]

    def player_move_key(self, k, screen_size):
        if k[K_d]:
            self.x_speed += 1.4
            self.pos = 'R'
        elif k[K_a]:
            self.x_speed -= 1.4
            self.pos = 'L'
        else:
            self.x_speed /= 1.1
            self.pos = 'M'
        if abs(self.x_speed) > 5:
            if self.x_speed > 0:
                self.x_speed = 5
            else:
                self.x_speed = -5
        self.x += self.x_speed
        if self.x+self.width > screen_size[0]:
            self.x = screen_size[0]-self.width
            self.pos = 'M'
        if self.x < 0:
            self.x = 0
            self.pos = 'M'


class Fire:
    def __init__(self, obj):
        self.x = obj.x
        self.y = obj.y
        self.img = ''
        self.animation = Animation({'fire': [4, 0.02]}, dirname(
            realpath(__file__))+'/assets/img/effects', 'fire', self)


class Animation():
    def __init__(self, sprites, path, first, obj):
        self.sprites = sprites
        self.path = path
        self.tile = first
        self.pos = 0
        self.last_update = time()
        self.obj = obj
        self.obj.img = pygame.image.load(
            path + '/' + first + str(self.pos) + '.png')

    def change(self, tile, pos=0):
        self.tile = tile
        self.pos = 0
        self.obj.img = pygame.image.load(
            self.path + '/' + tile + str(pos) + '.png')

    def update(self):
        if time()-self.last_update > self.sprites[self.tile][1]:
            if self.pos == self.sprites[self.tile][0]-1:
                self.pos = 0
            else:
                self.pos += 1
            self.obj.img = pygame.image.load(
                self.path + '/' + self.tile + str(self.pos) + '.png')
            self.last_update = time()


class Background:
    def __init__(self):
        self.x = -25
        self.y = 0
        self.tile = 0
        self.time = time()
        self.img = []
        path = dirname(realpath(__file__))
        for i in range(200):
            self.img.append(pygame.image.load(
                path+'/assets/img/bg/b0553b276f5049bec4808d6a012e32bc-' + str(i)+'.png'))


main()
