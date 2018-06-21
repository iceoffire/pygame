import pygame
from pygame.locals import *

from os.path import dirname, realpath

def main():
	running, settings = load()
	while running:
		settings = update(settings)
		draw(**settings)
		running = check_exit(**settings)
	pygame.quit()
	quit()

def load():
	screen_size = (600,400)
	screen = pygame.display.set_mode(screen_size)
	game_object = {
		'player' : [],
		'world'  : [],
		
	}
