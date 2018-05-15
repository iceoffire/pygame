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

def load_vars():
	global screen_size, screen, game_object, folder, cam, contador
	folder = os.path.dirname(os.path.realpath(__file__))
	screen_size = (600, 600)
	screen = pygame.display.set_mode(screen_size)
	contador = 0
	game_object = {'bg' : [Sprite(0, 0, "/assets/img/tiles/bg.png")],
		'HUD'   : [],
		'tiles' : [],
		'enemy' : [],
		'player': [],
		
	}
	print(game_object)
	cam = Camera(-screen_size[0]/2, -screen_size[1]/2)

def update():
	k = pygame.key.get_pressed()
	if k[K_d]:
		cam.x += 5
	elif k[K_a]:
		cam.x -= 5
	if k[K_s]:
		cam.y += 5
	elif k[K_w]:
		cam.y -= 5
	pass

def draw():
	screen.fill((0, 0, 0))
	camera()
	pygame.display.flip()
	fps(60)
	pass

def fps(frames):
	pygame.time.Clock().tick(frames)

def camera():
	global contador
	x = cam.x

	y = cam.y
	image_teste = game_object['tiles'][0].img
	for name in game_object:
		if contador < 5:
			print(name)
			contador +=1
		for gO in game_object[name]:
			temp_img = gO.img #pygame.transform.scale(gO.img, (160,160))
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
	for linha in range(height):
		for coluna in range(width):
			color = img.get_at((linha, coluna))
			load_object(str(color), linha*128, coluna*128)
	pass

def load_object(color, x, y):
	objects = {
		'(0, 0, 0, 255)'       : ['tiles','/assets/img/tiles/floor.png'], #black
	}
	if color in objects:
		game_object[objects[color][0]].append(Sprite(x, y, objects[color][1]))

#Classes
class Sprite():
	def __init__(self, x, y, path, scale=1, width=None, height=None):
		self.x = x
		self.y = y
		self.img = pygame.image.load(folder + path)
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
		self.is_grounded = False
	def move():
		if not Collider.check_floor_and_top:
			self.y += self.y_speed
		if not Collider.check_sides:
			self.x += self.x_speed

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
		self.scale = 1
	def move(x, y):
		self.x = x
		self.y = y

main()

