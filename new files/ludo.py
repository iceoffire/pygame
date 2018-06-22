import pygame
from pygame.locals import *
from pygame import gfxdraw

def main():
    running, settings = load()
    while running:
        settings = update(settings)
        draw(**settings)
        running = check_exit(**settings)
    pygame.quit()
    quit()

def load():
    screen_size = (500, 500)
    screen = pygame.display.set_mode(screen_size)
    surface = load_all(screen_size)
    return True, {
        'screen_size'   : screen_size,
        'screen'        : screen,
        'surface'       : surface,
        'exit_request'  : False,
    }

def update(settings):
    for e in pygame.event.get():
        if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
            settings['exit_request'] = True
    return settings

def draw(screen_size, screen, surface, **kwargs):
    screen.fill((0,0,0))
    screen.blit(surface, (0,0))
    pygame.display.flip()
    pass

def check_exit(exit_request, **kwargs):
    return not exit_request

def load_all(screen_size):
    surface = pygame.Surface(screen_size).convert_alpha()
    surface.fill((0,128,0))
    max_x = screen_size[0]-55-screen_size[0]*.3
    max_y = screen_size[1]-55-screen_size[0]*.3
    surface.blit(bg(screen_size), (10,10))
    
    players = (
        ((94,155,13), (25,25)),
        ((243,125,0), (max_x,25)),
        ((0,90,206) , (max_x,max_y)),
        ((201,0,8)  , (25,max_y)),
        
    )

    width = screen_size[0]*0.9/15
    height= screen_size[1]*0.9/15


    point_list = (
        (25+width*1, 25+height*6),
        (25+width*1, 25+height*8),
        (25+width*6, 25+height*8),
        (25+width*6, 25+height*7),
        (25+width*2, 25+height*7),
        (25+width*2, 25+height*6),
    )
    pygame.draw.polygon(surface, players[0][0], point_list)

    point_list = (
        (25+width*7, 25+height*1),
        (25+width*9, 25+height*1),
        (25+width*9, 25+height*2),
        (25+width*8, 25+height*2),
        (25+width*8, 25+height*6),
        (25+width*7, 25+height*6),
    )
    pygame.draw.polygon(surface, players[1][0], point_list)

    point_list = (
        (25+width*(15-1), 25+height*(15-6)), #inversao a partir de 15-index
        (25+width*(15-1), 25+height*(15-8)),
        (25+width*(15-6), 25+height*(15-8)),
        (25+width*(15-6), 25+height*(15-7)),
        (25+width*(15-2), 25+height*(15-7)),
        (25+width*(15-2), 25+height*(15-6)),
    )
    pygame.draw.polygon(surface, players[2][0], point_list)

    point_list = (
        (25+width*(15-7), 25+height*(15-1)),
        (25+width*(15-9), 25+height*(15-1)),
        (25+width*(15-9), 25+height*(15-2)),
        (25+width*(15-8), 25+height*(15-2)),
        (25+width*(15-8), 25+height*(15-6)),
        (25+width*(15-7), 25+height*(15-6)),
    )
    pygame.draw.polygon(surface, players[3][0], point_list)

    surface = make_lines(surface, screen_size)

    x = int((screen_size[0]-25)/14.0*6)+3
    y = int((screen_size[1]-25)/14.0*6)+3

    pygame.draw.rect(surface, (255,255,255), (x,y, 89,89))

    p = (
        ((width*7, height*7+5), 90),        #green
        ((width*7+4, height*7), 0),         #yellow
        ((width*8.5+1, height*7+4), 270),   #blue
        ((width*7+5, height*8.5+1),180),    #red
    )

    for i in range(4):
        tri = triangle(int(width*2.75)-10, int(height*1.5)-10, players[i][0])
        tri = pygame.transform.rotate(tri, p[i][1])
        surface.blit(tri, p[i][0])

    for i in range(4):
        surface.blit(base(players[i][0], screen_size), players[i][1])
    return surface

def triangle(width, height, color):
    surface = pygame.Surface((width, height)).convert_alpha()
    surface = alpha(surface)
    point_list = (
        (0,0),
        (width, 0),
        (width/2, height)
    )
    pygame.draw.polygon(surface, color, point_list)
    return surface

def alpha(surface):
    for i in range(surface.get_height()):
        for j in range(surface.get_width()):
            surface.set_at((j, i), (0,0,0,0))
    return surface

def make_lines(surface, screen_size):
    for i in range(16):
        x = 25+(i/15.0*screen_size[0]*0.9)
        y = 25+(i/15.0*screen_size[1]*0.9)
        pygame.draw.line(surface, (0,0,0), (x, 25), (x, screen_size[0]-25))
        pygame.draw.line(surface, (0,0,0), (25, y), (screen_size[1]-25, y))
    return surface

def bg(screen_size):
    x,y = [int(foo*0.1) for foo in screen_size]
    width,height = [int(foo-20) for foo in screen_size]
    surface = pygame.Surface((width, height))
    surface.convert_alpha()

    for row in range(height):
        for column in range(width): #cria o sombreado (hard work aqui)
            height_p1= min(row/(height*0.02), 1)
            height_p2= min(1-float(row-height*0.98)/(height*0.02), 1) 
            height_p = min(height_p1, height_p2)

            width_p1 = min(column/(width*0.02), 1)                     #aqui acontece uma matematica pra criar um gradiente radial
            width_p2 = min(1-float(column-width*0.98)/(width*0.02), 1) #tem que calcular 2 lados pra ele criar dos 2 lados
            width_p  = min(width_p1, width_p2)

            rgba = tuple([max(int(x*min(width_p, height_p)), 40) for x in (255,255,255)]) #pesado
            surface.set_at((column, row), rgba)

    return surface

def base(color, screen_size): #desenha a base de cada pessoa de acordo com a cor
    width = int((screen_size[0]-25)/14.0*5.0+25.0/2)-1
    height= int((screen_size[1]-25)/14.0*5.0+25.0/2)-1
    surface = pygame.Surface((width, height))
    surface.convert_alpha() #tinha um gradiente, mas foi desligado por ficar feio
    pygame.draw.rect(surface, (0,0,0), (0,0, width, height))
    pygame.draw.rect(surface, color, (1,1, width-2, height-2))
    pygame.draw.rect(surface, (255,255,255), (width*.2, height*.2, width*.6+1, height*.6+1))
    color = tuple([min(255, x+60) for x in color])
    for i in range(2):
        for j in range(2):
            x = width*0.2 +10+width*0.275*j
            y = height*0.2+10+height*0.275*i
            pygame.draw.rect(surface, color, (int(x),int(y), width*0.225, height*0.225))

            pygame.gfxdraw.aacircle(surface, int(x+width*0.225/2),int(y+height*0.225/2), 16, tuple([255-foo for foo in color]))
            pygame.gfxdraw.filled_circle(surface, int(x+width*0.225/2),int(y+height*0.225/2), 16, tuple([255-foo for foo in color]))
    return surface

if __name__=='__main__':
    main()
