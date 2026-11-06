"""Short-lived visual effects: explosions and muzzle flashes."""
import settings
from game import assets
from game.animation import Animation

EXPLOSION_FRAMES = "images/effects/explosion_{:02d}.png"
PLAYER_FLASH_FRAMES = "images/effects/muzzle_flash_player_{:02d}.png"
ENEMY_FLASH_FRAMES = "images/effects/muzzle_flash_enemy_{:02d}.png"


class Explosion:
    def __init__(self, center):
        self.animation = Animation(
            assets.frames(EXPLOSION_FRAMES, 8), settings.EXPLOSION_FRAME_TIME, loop=False
        )
        self.rect = self.animation.image.get_frect(center=center)

    @property
    def alive(self):
        return not self.animation.finished

    def update(self, dt):
        self.animation.update(dt)

    def draw(self, surface):
        surface.blit(self.animation.image, self.rect.topleft)


class MuzzleFlash:
    """Flash at a gun barrel. It follows its owner (anything with a .rect) while it plays."""

    def __init__(self, owner, offset, from_player):
        frames = PLAYER_FLASH_FRAMES if from_player else ENEMY_FLASH_FRAMES
        self.animation = Animation(
            assets.frames(frames, 7), settings.MUZZLE_FLASH_FRAME_TIME, loop=False
        )
        self.owner = owner
        self.offset = offset

    @property
    def alive(self):
        return not self.animation.finished

    def update(self, dt):
        self.animation.update(dt)

    def draw(self, surface):
        x = self.owner.rect.x + self.offset[0]
        y = self.owner.rect.y + self.offset[1]
        surface.blit(self.animation.image, (x, y))
