"""Square debris that flies out of a broken brick, falls and shrinks."""
import random

import pygame

GRAVITY = 600  # px / s^2


class Particle:
    def __init__(self, pos, color):
        self.pos = pygame.Vector2(pos)
        self.velocity = pygame.Vector2(random.uniform(60, 220), 0).rotate(random.uniform(0, 360))
        self.color = color
        self.life = self.max_life = random.uniform(0.35, 0.7)
        self.size = random.uniform(3, 6)

    def update(self, dt):
        self.life -= dt
        self.velocity.y += GRAVITY * dt
        self.pos += self.velocity * dt

    def draw(self, surface, offset):
        size = self.size * max(0.0, self.life / self.max_life)
        if size >= 1:
            rect = pygame.FRect(0, 0, size, size)
            rect.center = (self.pos.x + offset[0], self.pos.y + offset[1])
            pygame.draw.rect(surface, self.color, rect)


class Particles:
    def __init__(self):
        self.items = []

    def burst(self, pos, color, count=14):
        self.items.extend(Particle(pos, color) for _ in range(count))

    def update(self, dt):
        for particle in self.items:
            particle.update(dt)
        self.items = [p for p in self.items if p.life > 0]

    def draw(self, surface, offset=(0, 0)):
        for particle in self.items:
            particle.draw(surface, offset)
