#joguinho pra criança jogar
import pygame as pg
from pg.locals import *
from time import time

def main():
	running = load()
	while running:
		update()
		draw()
		running = check_exit()
	pg.quit()

def load():
	load_vars()
	load_config()
	pass

def load_vars():
	global screen_size, screen, game_object, config
	screen_size = (400, 400)
	screen = pg.display.set_caption(screen_size)
	game_object = {
		'HUD'   : [],
		'notas' : [],
		'cifra' : []
	}
	config = {
		'level'           : 0,
		'time_init'       : time(),
		'delta_time'      : 0,
		'time_accumulated': 0
	}
	pass

def load_config():
	#Notas até 0-3
	global tempo
	game_object['cifra'] = [[0, 1, 3, 2, 1, 2, 1]]
	tempo = 1


def update():
	for partitura in game_object['cifra']: #vai nota por nota na cifra
		for nota in partitura:
			carregar_nota(nota) #carrega nota
			while time()-config['time_init']<1: #espera 1 segundo para nascer uma nova nota
				move_notas() #atualiza Y das notas
	pass

def draw():
	pass

def check_exit():
	k = pg.key.get_pressed()
	for e in pg.event.get():
		if e.type==QUIT or k[K_ESCAPE]:
			return False
	return True

main()
