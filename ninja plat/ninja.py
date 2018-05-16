import pygame, os
from pygame.locals import *

def main():
	running = load()
	while running:
		update()
		draw()
		running = check_exit()
	pygame.quit()

def load():
	load_vars()
	load_map(1)
	return True

def update_anim():
	path_init = '/assets/img/player'
	#pegar o atual
	#concatenar status + num
	#idle0 - idle1
	#attacking0~3 = isso vai atualizar e tera prioridade

def load_vars():
	global screen_size, screen, game_object, folder, cam, camera_labels
	folder = os.path.dirname(os.path.realpath(__file__))
	screen_size = (800, 600)
	screen = pygame.display.set_mode(screen_size)
	
	game_object = {
		'bg' 		: [Sprite(0, 0, 'bg')],
		'tiles'		: [],
		'enemy'		: [],
		'player'	: [],
		'objective'	: []
	}
	cam = Camera(-screen_size[0], -screen_size[1])

def update():
	update_keys()
	#cam.set_focus((game_object['player'][0].x, game_object['player'][0].y)) ATIVAR QUANDO TIVER O PLAYER
	pass

def update_keys():
	k = pygame.key.get_pressed()
	if k[K_SPACE]:
		cam.set_focus((10, 10))
	if k[K_d]:
		cam.x -= 12
	elif k[K_a]:
		cam.x += 12
	if k[K_s]:
		cam.y -= 12
	elif k[K_w]:
		cam.y += 12
	if k[K_UP]:
		cam.set_scale(cam.scale+0.1)
	elif k[K_DOWN]:
		cam.set_scale(cam.scale-0.1)

def draw():
	screen.fill((0, 0, 0))
	camera()
	pygame.display.flip()
	fps(60)
	pass

def fps(frames):
	pygame.time.Clock().tick(frames)

def camera():
	image_teste = game_object['tiles'][0].img
	label = ['bg', 'tiles', 'enemy', 'player', 'objective']
	for i in label:
		for gO in game_object[i]:
			if i=='bg':
				screen.blit(gO.img, (0, 0))
			else:
				x = cam.x+cam.middle_screen[0]+gO.x*cam.scale-gO.x
				y = cam.y+cam.middle_screen[1]+gO.y*cam.scale-gO.y
				temp_img = pygame.transform.scale(gO.img, (int(gO.width*cam.scale+1), int(gO.height*cam.scale+1)))
				screen.blit(temp_img, (gO.x+x, gO.y+y))
#			screen.blit(image_teste, (gO.x+x, gO.y+y))

def check_exit():
	k = pygame.key.get_pressed()
	for e in pygame.event.get():
		if e.type==QUIT or k[K_ESCAPE]:
			return False
	return True

def load_map(map):
	path = "/assets/img/map/map" + str(map) + ".png"
	img = pygame.image.load(folder + path)
	width = img.get_width()
	height= img.get_height()
	cam.middle_screen = [width/2, height/2]
	for linha in range(height):
		for coluna in range(width):
			color = img.get_at((linha, coluna))
			load_object(str(color), linha*128, coluna*128, linha, coluna, img)
	pass

def load_object(color, x, y, px, py, img):
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
		'(0, 0, 255)'			: ['player', '/assets/img/player/idle0.png']
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
		game_object[objects[color][0]].append(Sprite(x, y, objects[color][0], objects[color][1]))

#Classes
class Sprite():
	def __init__(self, x, y, tipo, path=None,scale=1, width=None, height=None):
		self.x = x
		self.y = y
		if path == None:
			path = get_path(tipo)
		self.img = pygame.image.load(folder + path)
		if tipo == 'bg':
			self.img = pygame.transform.scale(self.img, screen_size)
		if width != None:
			self.width = width
		else:
			self.width = self.img.get_width()
		if height != None:
			self.height = height
		else:
			self.height = self.img.get_height()
		self.x_speed = 0
		self.y_speed = 0
		self.animation_status = 'idle'
		self.animation_count = 0
		self.is_grounded = False
	def change_to_animation(self, new_status, new_count):
		self.animation_status = new_status
		self.animation_count = count
		self.img = pygame.image.load(folder + '/assets/img/player/' + new_status + '.png')
	def move():
		for name in game_object:
			for gO in game_object[name]:
				if not Collider.check_floor_and_top(gO):
					gO.y += gO.y_speed
				if not Collider.check_sides(gO):
					gO.x += gO.x_speed

def get_path(tipo):
	img = {
		'enemy' : ['/assets/img/tile'],
		'bg'	: ['/assets/img/tiles/bg.png'],
		'player': [''],
		'tiles' : ["/assets/img/tiles/floor.png"]}
	return img[tipo][0]

class Collider():
	def check_floor_and_top(self, game_objects): #Vertical Sides
		for name in game_objects:
			for gO in game_objects[name]:
				if gO != self:
					pass
		return True
	def check_sides(self, game_objects): #Horizontal Sides
		return True

class Camera():
	def __init__(self, x_offset, y_offset):
		self.x_offset = x_offset
		self.y_offset = y_offset
		self.x = 0
		self.y = 0
		self.middle_screen = [0, 0]
		self.scale = 1
	def move(self, x, y):
		self.x = x
		self.y = y
	def set_scale(self, scale):
		if scale<0.1:
			scale = 0.1
		self.scale = scale
		self.middle_screen[0] *= scale
		self.middle_screen[1] *= scale
	def set_focus(self, (x, y)):
		if abs(x-self.x)>10:
			self.x /= 1.1
		else:
			self.x = x
		if abs(y-self.y)>10:
			self.y /= 1.1
		else:
			self.y = y

main()

