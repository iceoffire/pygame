"""The ninja: running, jumping (coyote time, buffering, variable height) and animation."""
import pygame

import settings
from game import assets
from game.animation import Animation
from game.physics import move_and_collide

FRAME_PATTERN = "images/player/{name}_{index:02d}.png"


class Player:
    def __init__(self, spawn_point):
        self.animation = Animation(FRAME_PATTERN, settings.PLAYER_ANIMATIONS, "idle")
        self.facing_left = False
        # Hitbox = the scaled sprite (80x104), like the original game.
        self.rect = pygame.FRect((0, 0), self.image.get_size())
        self.reset(spawn_point)

    def reset(self, spawn_point):
        """Stand still at `spawn_point` (mid-bottom position)."""
        self.rect.midbottom = spawn_point
        self.velocity = pygame.Vector2()
        self.facing_left = False
        self.grounded = False
        self.coyote_time = 0.0
        self.jump_buffer = 0.0
        self.jump_held = False
        self.animation.play("idle")

    # --- input ----------------------------------------------------------
    def press_jump(self):
        self.jump_buffer = settings.JUMP_BUFFER_TIME
        self.jump_held = True

    def release_jump(self):
        """Variable jump height: letting go early cuts the upward speed."""
        self.jump_held = False
        if self.velocity.y < 0:
            self.velocity.y *= settings.JUMP_CUT

    # --- simulation -----------------------------------------------------
    def update(self, dt, direction, level):
        """direction: -1 left, 0 none, +1 right."""
        self._run(dt, direction)
        self._jump(dt)

        # Gravity, integrated exactly (average of old and new speed) so the jump
        # reaches the same height at any frame rate.
        old_vy = self.velocity.y
        self.velocity.y = min(old_vy + settings.GRAVITY * dt, settings.MAX_FALL_SPEED)
        dy = (old_vy + self.velocity.y) / 2 * dt

        hits = move_and_collide(self.rect, self.velocity.x * dt, dy, level)
        if hits.wall:
            self.velocity.x = 0
        if hits.ceiling and self.velocity.y < 0:
            self.velocity.y = 0
        self.grounded = hits.floor
        if hits.floor and self.velocity.y > 0:
            self.velocity.y = 0

        # Side walls of the map (there is nothing to stand on outside it).
        if self.rect.left < 0:
            self.rect.left = 0
            self.velocity.x = 0
        elif self.rect.right > level.width:
            self.rect.right = level.width
            self.velocity.x = 0

        self._animate(dt, direction)

    def _run(self, dt, direction):
        if direction:
            self.velocity.x += direction * settings.RUN_ACCEL * dt
            self.velocity.x = max(-settings.MAX_RUN_SPEED, min(self.velocity.x, settings.MAX_RUN_SPEED))
            self.facing_left = direction < 0
        else:
            self.velocity.x /= settings.STOP_DAMPING ** (dt * 60)
            if abs(self.velocity.x) < settings.STOP_SPEED:
                self.velocity.x = 0

    def _jump(self, dt):
        # Coyote time: being grounded last frame "charges" a short jump window.
        self.coyote_time = settings.COYOTE_TIME if self.grounded else max(0.0, self.coyote_time - dt)
        if self.jump_buffer > 0 and self.coyote_time > 0:
            self.velocity.y = -settings.JUMP_SPEED
            if not self.jump_held:  # buffered tap that was already released: short hop
                self.velocity.y *= settings.JUMP_CUT
            self.jump_buffer = 0.0
            self.coyote_time = 0.0
            self.grounded = False
        else:
            self.jump_buffer = max(0.0, self.jump_buffer - dt)

    def _animate(self, dt, direction):
        if not self.grounded:
            self.animation.play("jumping")
        elif direction:
            self.animation.play("running")
        else:
            self.animation.play("idle")
        self.animation.update(dt)

    # --- drawing --------------------------------------------------------
    @property
    def image(self):
        return assets.scaled(self.animation.frame_name, settings.PLAYER_SCALE, self.facing_left)

    def draw(self, surface, offset):
        surface.blit(self.image, (round(self.rect.x) - offset[0], round(self.rect.y) - offset[1]))
