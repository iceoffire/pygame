"""Animated 200-frame space background, shifted horizontally with the player for parallax."""
import settings
from game import assets

FRAME_PATH = "images/background/frame_{:03d}.png"


class Background:
    def __init__(self):
        self.index = 0
        self.time = 0.0
        self.x = 0.0

    @property
    def image(self):
        # Frames load lazily through the cache, so startup doesn't stall on 200 PNGs.
        return assets.image(FRAME_PATH.format(self.index), alpha=False)

    def update(self, dt, player_x):
        self.time += dt
        while self.time >= settings.BACKGROUND_FRAME_TIME:
            self.time -= settings.BACKGROUND_FRAME_TIME
            self.index = (self.index + 1) % settings.BACKGROUND_FRAMES
        # The image is 50 px wider than the screen; the player's x slides it left.
        self.x = -player_x * settings.BACKGROUND_PARALLAX

    def draw(self, surface):
        surface.blit(self.image, (self.x, 0))
