import pygame
from pygame.locals import *
from math import sin,cos,radians
import math


def main():
    settings, playing = load()
    while playing:
        settings = update(settings)
        draw(**settings)
        playing = check_exit(settings['exit'])
    pygame.quit()

def load():
    screen_size = (400, 400)
    scene = pygame.display.set_mode(screen_size)
    bola = GameObject(30, 250, 20)
    return {
        'screen' : scene,
        'bola' : bola,
        'exit' : False,
    }, True

def update(settings):
    k = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == QUIT or k[K_ESCAPE]:
            settings['exit'] = True
        if k[K_r]:
            settings['bola'].x = 30
            settings['bola'].y = 250
            settings['bola'].gravidade = False
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            pos = pygame.mouse.get_pos()
            if settings['bola'].gravidade == False: #so entra aqui se a bola estiver parada
                settings['bola'].gravidade = True 
                hipotenusa = (((settings['bola'].x-pos[0])**2)+((settings['bola'].y-pos[1])**2))**0.5 #descobre a hipotenusa pra ver quanto forte ira jogar
                print(hipotenusa)
                settings['bola'].delta_x = (-hipotenusa/10.0)*sin(math.atan2(settings['bola'].x-pos[0], settings['bola'].y-pos[1])) # faz os calculos pra jogar a bola na direcao do mouse
                settings['bola'].delta_y = (-hipotenusa/10.0)*cos(math.atan2(settings['bola'].x-pos[0], settings['bola'].y-pos[1]))
    if settings['bola'].gravidade:
        settings['bola'].x += settings['bola'].delta_x #atualiza as posicoes
        settings['bola'].y += settings['bola'].delta_y
        settings['bola'].delta_y += 1 #acelera a gravidade
        settings['bola'].delta_x *= 0.98 #desacelera a bola no eixo X
            
    return settings

def draw(screen, bola, **kwargs):
    m_pos = pygame.mouse.get_pos()
    screen.fill((0,0,0))
    pygame.draw.aaline(screen, (255,255,0), (30, 250), (m_pos[0], m_pos[1]))
    pygame.draw.circle(screen, (255,255,255), (int(bola.x), int(bola.y)), bola.raio)
    pygame.display.flip()
    fps(60)
    pass

def fps(frames):
    pygame.time.Clock().tick(frames)

def check_exit(exit_r):
    return not exit_r

class GameObject:
    def __init__(self, x, y, raio):
        self.x = x
        self.y = y
        self.delta_x = 0
        self.delta_y = 0
        self.raio = raio
        self.gravidade = False

if __name__=='__main__':
    main()
