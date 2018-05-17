import pygame, os #import padrao

#import de classes
from Sprite          import * #probaly working
from Animation       import * #probaly working
from Collider2D_AABB import * #nao sei se ta funcionando, acho que nao


#import de variaveis
from pygame.locals   import *
from time            import time


def main():
    init = time()
    running, settings = load()
    print('load: ' + str(time()-init))
    init = time()
    while running:
        init = time()
        settings = update(settings)
        print('update   : ' + str(time()-init))
        init = time()
        draw(settings)
        print('draw     : ' + str(time()-init))
        init = time()
        running = check_exit()
        print('running  : ' + str(time()-init))
    pygame.quit()

#load
def load():
    settings = load_settings()
    settings['game_object'] = load_game_object(settings['game_object'], settings['var']['folder'])
    settings['game_object'] = load_map(settings, 1)
    running = True
    return running, settings
    
def load_map(settings, what_map):
    max_maps = settings['var']['total_maps']
    folder   = settings['var']['folder']
    if what_map > max_maps:
        load_scene('win_game')
    img = pygame.image.load(folder+ '/assets/img/map/map' + str(what_map) + '.png')
    width = img.get_width()
    height = img.get_height()
    for coluna in range(width):
        for linha in range(height):
            x = coluna
            y = linha
            color = str(img.get_at(x, y))
            load_object(settings['game_object'], color, x*128, y*128, x, y, img)
            
def load_scene(what_scene):
    pass

def load_settings():
    screen_size = (700, 550)
    screen = pygame.display.set_mode(screen_size)
    game_object = {
        'player'    : [],
        'tile'      : [],
        'collider'  : [],
        'bg'        : [],
        'camera'    : []
    }
    var = {
        'folder'    : os.path.dirname(os.path.realpath(__file__)),
        'total_maps': len(os.listdir(os.path.dirname(os.path.realpath(__file__)) + '/assets/img/map'))

    }
    return {
        'screen_size'   : screen_size,
        'screen'        : screen,
        'game_object'   : game_object,
        'var'           : var,
        'layers'        : ['bg', 'tile', 'player']
    }

def load_object(game_object, color, x, y, px, py, img):
	imagem = img
	color_left = ""
	color_right = ""
	color_up = ""
	color_down = ""
	if px>0:
		color_left = str(img.get_at((px-1, py)))
	if px<img.get_width()-1:
		color_right = str(img.get_at((px+1, py)))
	if py>0:
		color_up = str(img.get_at((px, py-1)))
	if py<img.get_height()-1:
		color_down = str(img.get_at((px, py+1)))
	objects = {
		'(0, 0, 0, 255)'       	: ['tiles', 'assets'],  #black
		'(255, 0, 0, 255)'		: ['objective', '/assets/img/tiles/objective.png'],
		'(0, 0, 255, 255)'		: ['player', '/assets/img/player/idle0.png']
	}
	if color == '(0, 0, 0, 255)':
		#especial aqui
		#floor Medio Up = FMU
		#FMF = Floor Medio Fly
		sufixo = 'F'

		#check sides
		if color_left!=color and color_left!="":
			sufixo += 'L'
		elif color_left==color and color_left == color_right:
			sufixo += 'M'
		elif color_left != color and color_right != color:
			sufixo += 'M'
		elif color_right != color:
			sufixo += 'R'
		elif color_left != color:
			sufixo += 'L'
		
		#check up&down
		if color_down == color and color != color_up: #
			sufixo += 'U'
		elif color_up == color:
			sufixo += 'D'
		elif color_down == "" and color_down==color_up:
			sufixo += 'U'
		elif color==color_up==color_down:
			sufixo += 'U'
		else:
			sufixo += 'F'
		sufixo += '.png'
		game_object[objects[color][0]].append(Sprite(x, y, objects[color][0], '/assets/img/tiles/'+sufixo))
	elif color in objects:
		if color=='(0, 0, 255, 255)':
			anim = { #player
                'idle'   : [2, 0.3],
                'running': [4, 0.2]
            }
            collider=(True, [0, 0, 128, 99])
            game_object['player'].append(Sprite((x, y), folder+'/assets/img/player/idle0.png', collider, (anim, folder+'/assets/img/player', 'idle'), 4))
		else:
			game_object[objects[color][0]].append(Sprite(x, y, objects[color][0], objects[color][1]))
    return game_object

def update(settings):
    game_object = settings['game_object']
    for name in game_object:
        for gO in game_object[name]:
            if gO.collider[0]:
                gO.collider[1].update_move(game_object)
    return settings

def draw(settings):
    game_object = settings['game_object']
    screen      = settings['screen']
    screen_size = settings['screen_size']
    layers      = settings['layers']

    screen.fill((0, 0, 0))
    camera(screen, screen_size, game_object, layers)
    pygame.display.flip()
    fps(60)
    pass

def fps(frames):
    pygame.time.Clock().tick(frames)

def camera(screen, screen_size, game_object, layers):
    for name in layers:
        for gO in game_object[name]:
            screen.blit(gO.img, (gO.x, gO.y))
        

def check_exit():
    k = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == QUIT or k[K_ESCAPE]:
            return False
    return True

if __name__=='__main__':
    main()