"""Smoothed camera that looks a little ahead of the player and stays inside the map."""
import pygame

import settings


class Camera:
    def __init__(self, screen_size, world_size):
        self.screen_size = pygame.Vector2(screen_size)
        self.world_size = pygame.Vector2(world_size)
        self.pos = pygame.Vector2()  # top-left corner of the view, in world pixels

    def change_screen_size(self, screen_size):
        self.screen_size = pygame.Vector2(screen_size)
        self.pos = self._clamp(self.pos)

    def _target(self, focus, look_ahead):
        return pygame.Vector2(
            focus[0] + look_ahead - self.screen_size.x / 2,
            focus[1] + settings.CAMERA_OFFSET_Y - self.screen_size.y / 2,
        )

    def _clamp(self, pos):
        """Keep the view inside the map; center the map if it's smaller than the screen."""
        clamped = pygame.Vector2(pos)
        for axis in (0, 1):
            room = self.world_size[axis] - self.screen_size[axis]
            clamped[axis] = room / 2 if room < 0 else min(max(clamped[axis], 0), room)
        return clamped

    def snap(self, focus):
        """Jump straight to `focus` (level start, respawn)."""
        self.pos = self._clamp(self._target(focus, 0))

    def follow(self, focus, look_ahead, dt):
        """Ease toward `focus`, shifted `look_ahead` pixels horizontally."""
        target = self._clamp(self._target(focus, look_ahead))
        # Frame-rate independent version of the old "move 1/10 of the way each frame".
        t = 1 - settings.CAMERA_SMOOTHING ** (dt * 60)
        self.pos += (target - self.pos) * t

    @property
    def offset(self):
        """Integer offset to subtract from world positions when drawing."""
        return round(self.pos.x), round(self.pos.y)

    @property
    def view(self):
        return pygame.FRect(self.pos.x, self.pos.y, self.screen_size.x, self.screen_size.y)
