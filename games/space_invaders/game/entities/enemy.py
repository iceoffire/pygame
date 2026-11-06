import random

import settings
from game import assets
from game.animation import Animation
from game.entities.player import THRUSTER_FRAMES


def enemy_path(kind):
    return f"images/enemies/enemy_{kind}.png"


class Enemy:
    def __init__(self, x, y, kind, speed):
        self.kind = kind  # 0, 1 or 2: sprite, HP and score
        self.hp = kind + 2
        self.speed = speed  # pixels per second, downward
        self.base_image = assets.image(enemy_path(kind))
        self.flash_image = self.base_image
        self.flash_time = 0.0
        self.rect = self.base_image.get_frect(topleft=(x, y))
        self.thruster = Animation(
            assets.frames(THRUSTER_FRAMES, 4), settings.THRUSTER_FRAME_TIME, start=random.randrange(4)
        )

    @property
    def alive(self):
        return self.hp > 0

    @property
    def score(self):
        return settings.ENEMY_SCORES[self.kind]

    @property
    def image(self):
        return self.flash_image if self.flash_time > 0 else self.base_image

    @property
    def on_screen(self):
        return self.rect.top >= 0

    def take_damage(self):
        self.hp -= 1
        self.flash_time = settings.ENEMY_HIT_FLASH_TIME
        color = random.choice(settings.ENEMY_HIT_FLASH_COLORS)
        self.flash_image = assets.tinted(enemy_path(self.kind), color)

    def update(self, dt):
        self.rect.y += self.speed * dt
        self.flash_time = max(0.0, self.flash_time - dt)
        self.thruster.update(dt)

    def draw(self, surface):
        # Enemies fly downward, so the engine flame sits on top of the sprite.
        surface.blit(self.thruster.image, (self.rect.x + 16, self.rect.y - 7))
        surface.blit(self.image, self.rect.topleft)
