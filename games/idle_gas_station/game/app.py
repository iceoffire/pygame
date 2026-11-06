"""Main loop: one window, one clock, one event queue, a stack of scenes."""
import os
import sys

import pygame

import settings

# Smoke-test hooks (see tools/smoke_test.py). Unset in normal play.
SMOKE_FRAMES = int(os.environ.get("SMOKE_FRAMES", "0"))
SMOKE_KEYS = (pygame.K_RETURN, pygame.K_SPACE, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_p, pygame.K_p, pygame.K_r)


def require_pygame_ce():
    if not getattr(pygame, "IS_CE", False):
        sys.exit(
            "This project needs pygame-ce, but the classic 'pygame' package is installed.\n"
            "Fix: pip uninstall pygame && pip install -r requirements.txt"
        )


class Game:
    def __init__(self, first_scene):
        require_pygame_ce()
        pygame.init()
        flags = 0 if os.environ.get("SDL_VIDEODRIVER") == "dummy" else pygame.SCALED
        self.screen = pygame.display.set_mode(settings.SCREEN_SIZE, flags)
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.scenes = []
        self.push(first_scene(self))

    # --- scene stack -------------------------------------------------
    @property
    def scene(self):
        return self.scenes[-1]

    def push(self, scene):
        self.scenes.append(scene)

    def pop(self):
        self.scenes.pop().on_exit()

    def switch(self, scene):
        """Replace the whole stack (e.g. Title -> Play, GameOver -> Play)."""
        self._exit_all()
        self.scenes = [scene]

    def _exit_all(self):
        """Give every scene on the stack a chance to clean up (the play scene saves here)."""
        for scene in reversed(self.scenes):
            scene.on_exit()

    def quit(self):
        self.running = False

    # --- loop --------------------------------------------------------
    def run(self):
        frame = 0
        while self.running:
            # Clamp dt so a stall (window drag, breakpoint) can't teleport objects.
            dt = min(self.clock.tick(settings.FPS) / 1000, 0.05)
            frame += 1
            if SMOKE_FRAMES:
                self._smoke_input(frame)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                else:
                    self.scene.handle_event(event)
            self.scene.update(dt)
            self.scene.draw(self.screen)
            pygame.display.flip()
        self._exit_all()
        pygame.quit()

    def _smoke_input(self, frame):
        if frame % 30 == 0:
            key = SMOKE_KEYS[(frame // 30) % len(SMOKE_KEYS)]
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=key, mod=0, unicode="", scancode=0))
            pygame.event.post(pygame.event.Event(pygame.KEYUP, key=key, mod=0, unicode="", scancode=0))
        if frame >= SMOKE_FRAMES:
            self.quit()
