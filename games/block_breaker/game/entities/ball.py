"""The ball: a square FRect for collisions, drawn as a circle.

Movement is split into small sub-steps, and each sub-step moves x then y, resolving
collisions after each axis. That way the ball never skips through a brick at high
speed, never bounces twice off the same brick, and always knows which side it hit.
"""
import math

import pygame

import settings

PLAY_AREA_LEFT = 0
PLAY_AREA_RIGHT = settings.SCREEN_WIDTH


class Ball:
    def __init__(self):
        size = settings.BALL_RADIUS * 2
        self.rect = pygame.FRect(0, 0, size, size)
        self.velocity = pygame.Vector2()
        self.speed = settings.BALL_SPEED_START
        self.launched = False

    # --- state -------------------------------------------------------
    def reset(self, paddle):
        """Back on the paddle at the starting speed (new life or new level)."""
        self.speed = settings.BALL_SPEED_START
        self.launched = False
        self.velocity.update(0, 0)
        self.stick_to(paddle)

    def stick_to(self, paddle):
        self.rect.midbottom = (paddle.rect.centerx, paddle.rect.top)

    def launch(self, direction):
        self.launched = True
        self.velocity = pygame.Vector2(0, -self.speed).rotate(settings.BALL_LAUNCH_ANGLE * direction)

    @property
    def lost(self):
        return self.rect.top > settings.SCREEN_HEIGHT

    # --- physics -----------------------------------------------------
    def update(self, dt, paddle, bricks):
        """Move the ball. Returns a list of (brick, destroyed) for every brick hit."""
        hits = []
        distance = self.velocity.length() * dt
        steps = max(1, math.ceil(distance / settings.BALL_MAX_STEP))
        step_dt = dt / steps
        for _ in range(steps):
            self._step_x(step_dt, bricks, hits)
            self._step_y(step_dt, paddle, bricks, hits)
        return hits

    def _step_x(self, dt, bricks, hits):
        self.rect.x += self.velocity.x * dt
        if self.rect.left < PLAY_AREA_LEFT:
            self.rect.left = PLAY_AREA_LEFT
            self.velocity.x = abs(self.velocity.x)
        elif self.rect.right > PLAY_AREA_RIGHT:
            self.rect.right = PLAY_AREA_RIGHT
            self.velocity.x = -abs(self.velocity.x)

        brick = self._closest_brick(bricks) if self.velocity.x else None
        if brick:
            if self.velocity.x > 0:
                self.rect.right = brick.rect.left
            else:
                self.rect.left = brick.rect.right
            self.velocity.x = -self.velocity.x
            hits.append((brick, brick.hit()))

    def _step_y(self, dt, paddle, bricks, hits):
        self.rect.y += self.velocity.y * dt
        if self.rect.top < settings.PLAY_TOP:
            self.rect.top = settings.PLAY_TOP
            self.velocity.y = abs(self.velocity.y)

        brick = self._closest_brick(bricks) if self.velocity.y else None
        if brick:
            if self.velocity.y > 0:
                self.rect.bottom = brick.rect.top
            else:
                self.rect.top = brick.rect.bottom
            self.velocity.y = -self.velocity.y
            hits.append((brick, brick.hit()))

        # Only bounce while falling and while the ball is above the paddle's middle:
        # a ball that is already rising (or clipped the side) can never get stuck inside.
        if (
            self.velocity.y > 0
            and self.rect.colliderect(paddle.rect)
            and self.rect.centery < paddle.rect.centery
        ):
            self._bounce_off_paddle(paddle)

    def _bounce_off_paddle(self, paddle):
        self.rect.bottom = paddle.rect.top
        self.speed = min(self.speed + settings.BALL_SPEED_STEP, settings.BALL_SPEED_MAX)
        # -1 at the left edge, 0 in the middle, 1 at the right edge.
        offset = (self.rect.centerx - paddle.rect.centerx) / (paddle.rect.width / 2)
        offset = max(-1.0, min(1.0, offset))
        self.velocity = pygame.Vector2(0, -self.speed).rotate(offset * settings.BALL_MAX_BOUNCE_ANGLE)

    def _closest_brick(self, bricks):
        """The one live brick this axis step should hit (nearest center), or None."""
        center = pygame.Vector2(self.rect.center)
        touching = [b for b in bricks if b.alive and self.rect.colliderect(b.rect)]
        if not touching:
            return None
        return min(touching, key=lambda b: center.distance_squared_to(b.rect.center))

    def draw(self, surface, offset=(0, 0)):
        center = (self.rect.centerx + offset[0], self.rect.centery + offset[1])
        pygame.draw.circle(surface, settings.BALL_COLOR, center, settings.BALL_RADIUS)
