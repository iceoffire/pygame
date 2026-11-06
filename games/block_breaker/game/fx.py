"""Small game-feel helpers: screen shake and floating text."""
import random

import pygame

from game import assets


class ScreenShake:
    def __init__(self):
        self.time = 0.0
        self.strength = 0.0

    def start(self, strength=4, duration=0.25):
        self.strength = max(self.strength, strength)
        self.time = max(self.time, duration)

    def update(self, dt):
        self.time = max(0.0, self.time - dt)
        if self.time == 0:
            self.strength = 0.0

    @property
    def offset(self):
        if not self.time:
            return (0, 0)
        s = self.strength
        return (random.uniform(-s, s), random.uniform(-s, s))


class FloatingText:
    """'+100' that drifts up and fades out."""

    def __init__(self, text, pos, color=(255, 255, 255), size=22, life=0.8):
        self.image = assets.font(size).render(text, True, color)
        self.pos = pygame.Vector2(pos)
        self.life = self.max_life = life

    @property
    def alive(self):
        return self.life > 0

    def update(self, dt):
        self.life -= dt
        self.pos.y -= 40 * dt

    def draw(self, surface, offset=(0, 0)):
        self.image.set_alpha(int(255 * max(0.0, self.life / self.max_life)))
        rect = self.image.get_rect(center=(self.pos.x + offset[0], self.pos.y + offset[1]))
        surface.blit(self.image, rect)
