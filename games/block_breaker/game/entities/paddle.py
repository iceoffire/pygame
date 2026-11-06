import pygame

import settings


class Paddle:
    def __init__(self):
        self.rect = pygame.FRect((0, 0), settings.PADDLE_SIZE)
        self.last_direction = 1  # -1 left, 1 right: used for the launch angle
        self.reset()

    def reset(self):
        self.rect.midtop = (settings.SCREEN_WIDTH / 2, settings.FLOOR_LEVEL)

    def move(self, direction, dt):
        if direction:
            self.last_direction = 1 if direction > 0 else -1
            self.rect.x += direction * settings.PADDLE_SPEED * dt
        self._clamp()

    def follow_mouse(self, x):
        if x != self.rect.centerx:
            self.last_direction = 1 if x > self.rect.centerx else -1
        self.rect.centerx = x
        self._clamp()

    def _clamp(self):
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(settings.SCREEN_WIDTH, self.rect.right)

    def draw(self, surface, offset=(0, 0)):
        rect = self.rect.move(offset)
        pygame.draw.rect(surface, settings.PADDLE_COLOR, rect)
        pygame.draw.rect(surface, settings.OUTLINE, rect, 1)
