import pygame, os, random
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
	global screen_size, screen, game_object, folder, cam, debug, teste, total_maps
	teste = 0
	folder = os.path.dirname(os.path.realpath(__file__))
	total_maps = len(os.listdir(folder + '/assets/img/map'))
	screen_size = (800, 600)
	screen = pygame.display.set_mode(screen_size)
	debug = True
	game_object = {
		'bg' 		: [Sprite(0, 0, 'bg')],
		'tiles'		: [],
		'enemy'		: [],
		'player'	: [],
		'objective'	: [],
		'collider' 	: []
	}
	cam = Camera(-screen_size[0], -screen_size[1])

def update():
	player = game_object['player'][0]
	update_keys()
	player.move()
	pass

def update_keys():
	global debug
	k = pygame.key.get_pressed()
	if k[K_c]:
		debug = -debug
		while k[K_c]:
			k = pygame.key.get_pressed()
	player = game_object['player'][0]
	if k[K_SPACE] and player.is_grounded:
		player.y_speed = -25
		player.is_grounded = False
	elif k[K_x]:
		cam.set_focus((850, 700), True)
	else:
		cam.set_focus((player.x-screen_size[0]/2+player.width/2, player.y-screen_size[1]/2+player.height)) #ATIVAR QUANDO TIVER O PLAYER
	if k[K_d]:
		player.x_speed+=2
	elif k[K_a]:
		player.x_speed-=2
	if k[K_s]:
		cam.move((cam.x, cam.y+32))
	elif k[K_w]:
		cam.move((cam.x, cam.y-32))
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
	layer = ['bg', 'tiles', 'enemy', 'player', 'objective']
	for i in layer:
		for gO in game_object[i]:
			x = -cam.x+cam.middle_screen[0]+gO.x*cam.scale-gO.x
			y = -cam.y+cam.middle_screen[1]+gO.y*cam.scale-gO.y
			if gO.x+x<screen_size[0]:
				if i=='bg':
					screen.blit(gO.img, (0, 0))
				else:
					temp_img = pygame.transform.scale(gO.img, (int(gO.width*cam.scale+1), int(gO.height*cam.scale+1)))
					screen.blit(temp_img, (gO.x+x, gO.y+y))
				if i=='player' and debug:
					pygame.draw.rect(screen, (255, 0, 0), (gO.x+x+10, gO.y+y, 30*cam.scale, 105*cam.scale), 1)
	if debug:
		for gO in game_object['collider']:
			x = -cam.x+cam.middle_screen[0]+gO.x*cam.scale-gO.x
			y = -cam.y+cam.middle_screen[1]+gO.y*cam.scale-gO.y
			pygame.draw.rect(screen, (255, 0, 0), (gO.x+x, gO.y+y, gO.width*cam.scale, gO.height*cam.scale), 1)

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
	cam.bounds = (width*128-screen_size[0], height*128-screen_size[1])
	cam.middle_screen = [width/2, height/2]
	for linha in range(height):
		for coluna in range(width):
			color = img.get_at((coluna, linha))
			load_object(str(color), coluna*128, linha*128, coluna, linha, img)
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
			game_object[objects[color][0]].append(Sprite(x, y, objects[color][0], objects[color][1], 4))
		else:
			game_object[objects[color][0]].append(Sprite(x, y, objects[color][0], objects[color][1]))

#Classes
class Sprite():
	def __init__(self, x, y, tipo, path=None,scale=1, width=None, height=None, collider=None):
		self.x = x
		self.y = y
		if path == None:
			path = get_path(tipo)
		self.img = pygame.image.load(folder + path)
		if scale!= None:
			self.img = pygame.transform.scale(self.img, (self.img.get_width()*scale, self.img.get_height()*scale))
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

		if collider!=None:
			pass
		self.x_speed = 0
		self.y_speed = 0
		self.animation_status = 'idle'
		self.animation_count = 0
		self.is_grounded = False
	def change_to_animation(self, new_status, new_count):
		self.animation_status = new_status
		self.animation_count = count
		self.img = pygame.image.load(folder + '/assets/img/player/' + new_status + '.png')
	def move(self):
		k = pygame.key.get_pressed()
		if self.x_speed > 10:
			self.x_speed = 10
		if self.x_speed < -10:
			self.x_speed = -10
		if not check_floor_and_top(self, game_object['tiles']):
			self.y += self.y_speed
			self.y_speed += 1
		else:
			self.y_speed = 0
		if not check_sides(self, game_object['tiles']):
			self.x += self.x_speed
		else:
			self.x_speed = 0
		if self.x<0:
			self.x = self.x_speed = 0
		if self.x>cam.bounds[0]+screen_size[0]-self.width:
			self.x = screen_size[0]+cam.bounds[0]-self.width
			self.x_speed = 0
		if not k[K_d] and not k[K_a]:
			self.x_speed /=3
			if abs(self.x_speed)<=1:
				self.x_speed = 0

def get_path(tipo):
	img = {
		'enemy' : ['/assets/img/tile'],
		'bg'	: ['/assets/img/tiles/bg.png'],
		'player': [''],
		'tiles' : ["/assets/img/tiles/floor.png"]}
	return img[tipo][0]

def check_floor_and_top(obj, game_objects): #Vertical Sides
	global teste
	bounds_x = obj.x+10
	bounds_y = obj.y
	bounds_width = obj.width-50
	bounds_height= obj.height
	for gO in game_objects: #1- top |2- bottom
		if bounds_y+bounds_height>gO.y+gO.height: #em baixo
			if (bounds_y+obj.y_speed<=gO.y+gO.height):
				if (bounds_x>gO.x and bounds_x<gO.x+gO.width) or \
				(bounds_x+bounds_width>gO.x and bounds_x+bounds_width< gO.x+gO.width)
					obj.y = gO.y+gO.height+1
					return True
		else: #em cima \ Aqui tem que testar se o objeto esta em cima
			if bounds_y+bounds_height<gO.y+gO.height:
				obj.y = gO.y-bounds_height
				obj.is_grounded = True
				return True
	return False

def verificar_se_esta_em_cima(origem, destino):
	if origem.y+origem.height<destino.y:
		return True

def check_sides(obj, game_objects): #Horizontal Sides
	bounds_x = obj.x+10
	bounds_y = obj.y
	bounds_width = obj.width-50
	bounds_height= obj.height
	for gO in game_objects:
		if len(game_object['collider']) < len(game_objects):
			game_object['collider'].append(box2D(gO.x, gO.y, gO.width, gO.height))
	for gO in game_objects:
		if (bounds_x+bounds_width>gO.x) and (bounds_x<gO.x+gO.width):
			if (bounds_y+bounds_height > gO.y and bounds_y < gO.y+gO.height):
				print('oi ' + str(random.randint(1,100)))
				obj.x = gO.x-bounds_width-10
				return True
	return False


class box2D():
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

class Camera():
	def __init__(self, x_offset, y_offset):
		self.x = 0
		self.y = 0
		self.bounds = (0, 0)
		self.middle_screen = [0, 0]
		self.scale = 1
	def move(self, (x, y)):
		self.x = x
		self.y = y
	def set_scale(self, scale):
		if scale<0.1:
			scale = 0.1
		self.scale = scale
		self.middle_screen[0] *= scale
		self.middle_screen[1] *= scale
	def set_focus(self, (x, y), ignore_bounds=False):
		if abs(self.x-x)>2:
			self.x = self.x+(x-self.x)/10
		else:
			self.x = x
		if abs(y-self.y)>2:
			self.y = self.y+(y-self.y)/10
		else:
			self.y = y
		if not ignore_bounds:
			self.check_sides()
	def check_sides(self):
		if self.x<0:
			self.x = 0
		elif self.x>self.bounds[0]:
			self.x = self.bounds[0]
		if self.y<0:
			self.y = 0
		elif self.y>self.bounds[1]:
			self.y = self.bounds[1]
	
main()

