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
	global screen_size, screen, game_object, folder, cam
	folder = os.path.dirname(os.path.realpath(__file__))
	screen_size = (300, 300)
	screen = pygame.display.set_mode(screen_size)
	game_object = {
		"player" : [],
		"bg"	 : [],
		"enemy"  : [],
		"HUD"    : []
	}
	cam = Camera(-screen_size[0]/2, -screen_size[1]/2)

def load_map(map):
	path = "/assets/img/map/map" + str(map) + ".png"
	img = pygame.image.load(folder + path)
	width = img.get_width()
	height= img.get_height()
	for linha in range(height):
		for coluna in range(width):
			color = img.get_at((linha, coluna))
			load_object(str(color), linha*32, coluna*32)
	pass

def load_object(color, x, y):
	objects = {
		'(0, 0, 0, 255)'       : ['bg','/assets/img/tiles/floor.png'], #black
		'(255, 255, 255, 255)' : ['bg','/assets/img/tiles/bg.png'], #white
	}
	if color in objects:
		game_object[objects[color][0]].append(Sprite(x, y, objects[color][1]))

def update():
	pass

def draw():
	screen.fill((0, 0, 0))
	camera()
	pygame.display.flip()
	pass

def camera():
	for name in game_object:
		for gO in game_object[name]:
			screen.blit(gO.img, (gO.x, gO.y))

def check_exit():
	k = pygame.key.get_pressed()
	for e in pygame.event.get():
		if e.type==QUIT or k[K_ESCAPE]:
			return False
	return True

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

