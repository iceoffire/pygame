"""Particle System: a torch that follows the mouse and emits additive fire particles."""
import math
import os
import random
import sys

import pygame

import settings

# Smoke-test hooks (see tools/smoke_test.py). Unset in normal play.
SMOKE_FRAMES = int(os.environ.get("SMOKE_FRAMES", "0"))


def require_pygame_ce():
    if not getattr(pygame, "IS_CE", False):
        sys.exit(
            "This project needs pygame-ce, but the classic 'pygame' package is installed.\n"
            "Fix: pip uninstall pygame && pip install -r requirements.txt"
        )


def additive_version(image):
    """Flatten an alpha image onto black so it can be drawn with BLEND_ADD.

    Black adds nothing, so transparent areas stay invisible and edges fade smoothly.
    """
    flat = pygame.Surface(image.get_size()).convert()
    flat.fill((0, 0, 0))
    flat.blit(image, (0, 0))
    return flat


class FireCache:
    """Scaled + dimmed copies of fire.png, built on first use and reused."""

    def __init__(self, image):
        self.base = image
        self.cache = {}

    def get(self, size, brightness):
        size = max(1, int(size))
        level = max(0, min(settings.BRIGHTNESS_LEVELS - 1, int(brightness * (settings.BRIGHTNESS_LEVELS - 1))))
        key = (size, level)
        surface = self.cache.get(key)
        if surface is None:
            scaled = pygame.transform.smoothscale(self.base, (size, size))
            surface = additive_version(scaled)
            k = int(255 * level / (settings.BRIGHTNESS_LEVELS - 1))
            surface.fill((k, k, k), special_flags=pygame.BLEND_MULT)
            self.cache[key] = surface
        return surface


class Particle:
    __slots__ = ("pos", "vel", "age", "lifetime", "start_size")

    def __init__(self, x, y, base_size):
        self.pos = pygame.Vector2(x + random.uniform(-settings.PARTICLE_JITTER_X, settings.PARTICLE_JITTER_X), y)
        speed = random.uniform(*settings.PARTICLE_SPEED)
        angle = math.radians(random.uniform(*settings.PARTICLE_ANGLE))
        self.vel = pygame.Vector2(speed * math.cos(angle), speed * math.sin(angle))
        self.age = 0.0
        self.lifetime = random.uniform(*settings.PARTICLE_LIFETIME)
        self.start_size = base_size * random.uniform(*settings.PARTICLE_SCALE)

    @property
    def progress(self):
        return self.age / self.lifetime

    def update(self, dt):
        self.age += dt
        self.pos += self.vel * dt
        return self.age < self.lifetime


class Demo:
    def __init__(self):
        require_pygame_ce()
        pygame.init()
        flags = 0 if os.environ.get("SDL_VIDEODRIVER") == "dummy" else pygame.SCALED
        self.screen = pygame.display.set_mode(settings.SCREEN_SIZE, flags)
        pygame.display.set_caption(settings.TITLE)
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, settings.FONT_SIZE)

        fire = pygame.image.load(settings.FIRE_IMAGE).convert_alpha()
        self.fire_size = fire.get_width()
        self.fire_cache = FireCache(fire)
        self.torch = pygame.transform.scale_by(pygame.image.load(settings.TORCH_IMAGE).convert_alpha(), settings.TORCH_SCALE)
        self.glow = additive_version(pygame.image.load(settings.GLOW_IMAGE).convert_alpha())

        self.particles = []
        self.spawn_rate = settings.SPAWN_RATE
        self.spawn_budget = 0.0
        self.running = True

    def run(self):
        frame = 0
        while self.running:
            dt = min(self.clock.tick(settings.FPS) / 1000, 0.05)
            frame += 1
            if SMOKE_FRAMES:
                self._smoke_input(frame)
            for event in pygame.event.get():
                self.handle_event(event)
            self.update(dt)
            self.draw()
            pygame.display.flip()
        pygame.quit()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.running = False
        elif event.type == pygame.MOUSEWHEEL:
            self.spawn_rate += event.y * settings.SPAWN_RATE_STEP
            self.spawn_rate = max(settings.SPAWN_RATE_MIN, min(settings.SPAWN_RATE_MAX, self.spawn_rate))

    def update(self, dt):
        self.particles = [p for p in self.particles if p.update(dt)]
        self.spawn_budget += self.spawn_rate * dt
        x, y = pygame.mouse.get_pos()
        while self.spawn_budget >= 1:
            self.spawn_budget -= 1
            if len(self.particles) < settings.MAX_PARTICLES:
                self.particles.append(Particle(x, y, self.fire_size))

    def draw(self):
        screen = self.screen
        screen.fill(settings.BACKGROUND_COLOR)
        mx, my = pygame.mouse.get_pos()

        glow_rect = self.glow.get_rect(center=(mx + settings.GLOW_OFFSET[0], my + settings.GLOW_OFFSET[1]))
        screen.blit(self.glow, glow_rect, special_flags=pygame.BLEND_ADD)
        torch_rect = self.torch.get_rect(midtop=(mx + settings.TORCH_OFFSET[0], my + settings.TORCH_OFFSET[1]))
        screen.blit(self.torch, torch_rect)

        for p in self.particles:
            t = p.progress
            image = self.fire_cache.get(p.start_size * (1 - t), (1 - t) ** 1.5)
            screen.blit(image, image.get_rect(center=(int(p.pos.x), int(p.pos.y))), special_flags=pygame.BLEND_ADD)

        text = f"Intensity: {self.spawn_rate} particles/s (mouse wheel)    Particles: {len(self.particles)}"
        screen.blit(self.font.render(text, True, settings.TEXT_COLOR), (8, 8))
        screen.blit(self.font.render("Esc: quit", True, settings.TEXT_COLOR), (8, 28))

    def _smoke_input(self, frame):
        if frame % 60 == 0:
            notch = 1 if (frame // 60) % 4 < 2 else -1
            pygame.event.post(pygame.event.Event(pygame.MOUSEWHEEL, x=0, y=notch, flipped=False,
                                                 precise_x=0.0, precise_y=float(notch)))
        if frame >= SMOKE_FRAMES:
            self.running = False


if __name__ == "__main__":
    Demo().run()
