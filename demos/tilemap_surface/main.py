"""Tilemap Surface: build one big surface from a tiny map image, then scale it to the window."""
import os
import sys

import pygame

import settings

# Smoke-test hooks (see tools/smoke_test.py). Unset in normal play.
SMOKE_FRAMES = int(os.environ.get("SMOKE_FRAMES", "0"))
SMOKE_KEYS = (pygame.K_2, pygame.K_1)


def require_pygame_ce():
    if not getattr(pygame, "IS_CE", False):
        sys.exit(
            "This project needs pygame-ce, but the classic 'pygame' package is installed.\n"
            "Fix: pip uninstall pygame && pip install -r requirements.txt"
        )


def build_level(map_path, floor_tile):
    """Every map pixel becomes a TILE_SIZE tile; FLOOR_COLOR pixels get the floor image."""
    layout = pygame.image.load(map_path)
    width, height = layout.get_size()
    size = settings.TILE_SIZE
    surface = pygame.Surface((width * size, height * size), 0, 32)  # 32-bit: smoothscale needs it
    surface.fill(settings.BACKGROUND_COLOR)
    for row in range(height):
        for column in range(width):
            if tuple(layout.get_at((column, row)))[:3] == settings.FLOOR_COLOR:
                surface.blit(floor_tile, (column * size, row * size))
    return pygame.transform.smoothscale(surface, settings.SCREEN_SIZE)


class Demo:
    def __init__(self):
        require_pygame_ce()
        pygame.init()
        flags = 0 if os.environ.get("SDL_VIDEODRIVER") == "dummy" else pygame.SCALED
        self.screen = pygame.display.set_mode(settings.SCREEN_SIZE, flags)
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, settings.FONT_SIZE)
        self.floor_tile = pygame.image.load(settings.FLOOR_TILE).convert_alpha()
        self.levels = {}   # map number -> built surface (built on first use)
        self.running = True
        self.select_map(1)

    def select_map(self, number):
        if number not in self.levels:
            self.levels[number] = build_level(settings.MAPS[number], self.floor_tile)
        self.current = number
        self.hint = self.render_shadowed(f"Map {number}    1 / 2: switch map    Esc: quit")

    def render_shadowed(self, text):
        front = self.font.render(text, True, settings.TEXT_COLOR)
        shadow = self.font.render(text, True, settings.SHADOW_COLOR)
        surface = pygame.Surface((front.get_width() + 2, front.get_height() + 2), pygame.SRCALPHA)
        surface.blit(shadow, (2, 2))
        surface.blit(front, (0, 0))
        return surface

    def run(self):
        frame = 0
        while self.running:
            self.clock.tick(settings.FPS)
            frame += 1
            if SMOKE_FRAMES:
                self._smoke_input(frame)
            for event in pygame.event.get():
                self.handle_event(event)
            self.draw()
            pygame.display.flip()
        pygame.quit()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.key in (pygame.K_1, pygame.K_KP1):
                self.select_map(1)
            elif event.key in (pygame.K_2, pygame.K_KP2):
                self.select_map(2)

    def draw(self):
        self.screen.blit(self.levels[self.current], (0, 0))
        self.screen.blit(self.hint, (10, 10))

    def _smoke_input(self, frame):
        if frame % 60 == 0:
            key = SMOKE_KEYS[(frame // 60) % len(SMOKE_KEYS)]
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=key, mod=0, unicode="", scancode=0))
            pygame.event.post(pygame.event.Event(pygame.KEYUP, key=key, mod=0, unicode="", scancode=0))
        if frame >= SMOKE_FRAMES:
            self.running = False


if __name__ == "__main__":
    Demo().run()
