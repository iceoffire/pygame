import pygame

import settings


class Brick:
    def __init__(self, rect, color, score, hp=1):
        self.rect = pygame.FRect(rect)
        self.base_color = color
        self.score = score
        self.hp = self.max_hp = hp

    @property
    def alive(self):
        return self.hp > 0

    @property
    def color(self):
        """Base gradient color on the last hit point, a warning color above that."""
        if self.hp > 1:
            colors = settings.BRICK_HP_COLORS
            return colors.get(self.hp, colors[max(colors)])
        return self.base_color

    @property
    def points(self):
        return self.score * self.max_hp

    def hit(self):
        """Take one hit. Returns True if this hit destroyed the brick."""
        self.hp -= 1
        return self.hp <= 0

    def draw(self, surface, offset=(0, 0)):
        rect = self.rect.move(offset)
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, settings.OUTLINE, rect, 1)
