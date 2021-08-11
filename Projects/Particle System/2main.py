#!/usr/bin/python3

from os.path import dirname, realpath
from math import cos, sin, tan, radians
from time import time, time_ns
from random import randint

from pygame import quit
from pygame.key import get_pressed
from pygame.image import img_load
from pygame.event import get
from pygame.time import Clock
from pygame.display import set_mode, flip
from pygame.transform import scale
from pygame.mouse import get_pos, set_visible
from pygame.locals import QUIT


def main():
    maior = {"update": 0, "draw": 0, "running": 0}
    soma = {"update": 0, "draw": 0, "running": 0}
    quant = 0
    running, settings = load()
    tempo = time_ns()
    print(f"load: {time_division(time_ns() - tempo)}")
    while running:
        quant += 1
        init = time_ns()
        #settings = update(settings)
        update(settings["game_object"], settings["var"])
        init, maior, soma = time_record(init, maior, soma, "update")
        
        draw(settings)
        init, maior, soma = time_record(init, maior, soma, "draw")
        
        running = check_exit(settings["var"]["exit_request"])
        init, maior, soma = time_record(init, maior, soma, "running")
        
    for key in maior:
        print(f"maior_{key}: {time_division(maior[key])}")
    for key in soma:
        print(f"media_{key}: {time_division(soma[key]/quant)}")
    quit()

def time_record(init, maior, soma, key):
    maior[key] = time_ns() - init if time_ns() - init > maior[key] else maior[key]
    soma[key] += time_ns() - init
    return time_ns(), maior, soma

TIMGINGS = {
    "seconds": 1000000000,
    "miliseconds": 1000000,
    "microseconds": 1000,
    "nanoseconds": 1}

def time_division(tm):
    global TIMGINGS
    return ", ".join([f"{tm // v} {k}" for k, v in TIMGINGS if tm // v > 1])

def load():
    screen_size = (500, 500)
    screen = set_mode(screen_size)
    set_visible(0)
    game_object = {"particles": list(), "tocha": list(), "shader": list()}
    var = {"folder": dirname(realpath(__file__)), "exit_request": False}
    img = {"fire": img_load(f"{var['folder']}/fire.png")}
    #fazer 240
    game_object["tocha"].append(Sprite((0, 0), f"{var['folder']/tocha.png", 1.4))
    game_object["shader"].append(Sprite((0, 0), f"{var['folder']/shader.png"))
    return True, {
        "screen_size": screen_size, "screen": screen,
        "game_object": game_object, "img": img, "var": var}

def update(game_object, var):
    for part in game_object["particles"]:
        part.x += part.delta_x
        part.y += part.delta_y
        part.size -= 2
        part.img = change_alpha(part.img, (part.width, part.height))
        if part.size <= 0 or part.img.get_at((8,8))[3] <= 10:
            game_object["particles"].remove(part)
    if len(game_object["particles"]) < 100:
        m_pos = get_pos()
        for _ in range(4):
            game_object["particles"].append(
                Particle((m_pos[0], m_pos[1]), f"{var['folder']}/fire.png"))

def draw(settings):
    screen = settings["screen"]
    game_object = settings["game_object"]
    img = settings["img"]
    screen.fill((20, 20, 20))
    m_pos = get_pos()
    for name in ["shader", "tocha"]:
        for game_obj in game_object[name]:
            if game_obj.__class__ == Sprite:
                if name == "shader":
                    screen.blit(
                        game_obj.img, (
                            m_pos[0] - game_obj.img.get_width() / 2 + 10,
                            m_pos[1] - game_obj.img.get_height() / 2 + 20))
                else:
                    screen.blit(game_obj.img, (m_pos[0] + 6, m_pos[1] + 15))
    for particle in game_object["particles"]:
        temp_img = scale(
            particle.img, (
                int(particle.img.get_width() * particle.size / 100),
                int(particle.img.get_height() * particle.size / 100))
            )
        screen.blit(temp_img, (particle.x, particle.y))
    
    flip()
    fps(60)

def fps(frames):
    Clock().tick(frames)

def change_alpha(img, (width, height)):
    for l in range(height):
        for c in range(width):
            img.set_at((l, c), divide_alpha(img.get_at((l, c))))
    return img

divide_alpha = lambda *rgb, a : *rgb, a / 1.2

def check_exit(request):
    if request:
        return False
    k = get_pressed()
    for event in get():
        if event.type == QUIT or event.type == k[K_ESCAPE]:
            return False
    return True

class Sprite():
    def __init__(self, (x, y), path, scale = 1):
        self.x = x
        self.y = y
        self.width = int(self.img.get_width() * scale)
        self.height = int(self.img.get_height() * scale)
        self.img = img_load(path)
        self.img = scale(self.img, (self.width, self.height))

class Particle():
    def __init__(self, (x, y), path):
        self.x = x + randint(-4, 3)
        self.y = y
        self.size = randint(50, 200)
        self.img = img_load(path)
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        speed = randint(150, 250) / 100
        angle = radians(randint(230, 310))
        self.delta_x = speed * cos(angle)
        self.delta_y = speed * sin(angle)

if __name__ == "__main__":
	main()
