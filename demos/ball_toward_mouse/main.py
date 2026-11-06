"""Ball Toward Mouse: click to throw a ball toward the mouse (oblique throw with gravity)."""
import os
import sys

import pygame

import settings

# Smoke-test hooks (see tools/smoke_test.py). Unset in normal play.
SMOKE_FRAMES = int(os.environ.get("SMOKE_FRAMES", "0"))


def require_pygame_ce():
    if not getattr(pygame, "IS_CE", False):
        sys.exit(
            "This project needs pygame-ce, but the classic 'pygame' package is installed.\n"
            "Fix: pip uninstall pygame && pip install -r requirements.txt"
        )


def step(pos, vel, h):
    """Advance one fixed physics step. Returns (pos, vel, on_floor). Shared by ball and preview."""
    width, height = settings.SCREEN_SIZE
    r = settings.BALL_RADIUS
    vel = pygame.Vector2(vel.x * settings.AIR_DRAG_X ** h, vel.y + settings.GRAVITY * h)
    pos = pos + vel * h
    on_floor = False
    if pos.y > height - r:
        pos.y = height - r
        vel.y = -vel.y * settings.RESTITUTION
        vel.x *= settings.FLOOR_FRICTION
        if abs(vel.y) < settings.REST_SPEED:
            vel.y = 0
        on_floor = True
    if pos.x < r:
        pos.x = r
        vel.x = -vel.x * settings.RESTITUTION
    elif pos.x > width - r:
        pos.x = width - r
        vel.x = -vel.x * settings.RESTITUTION
    return pos, vel, on_floor


def is_resting(vel, on_floor):
    return on_floor and vel.length() < settings.REST_SPEED


class Demo:
    def __init__(self):
        require_pygame_ce()
        pygame.init()
        flags = 0 if os.environ.get("SDL_VIDEODRIVER") == "dummy" else pygame.SCALED
        self.screen = pygame.display.set_mode(settings.SCREEN_SIZE, flags)
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, settings.FONT_SIZE)
        self.hint = self.font.render("Click to throw    R: reset    Esc: quit", True, settings.TEXT_COLOR)
        self.running = True
        self.reset()

    def reset(self):
        self.pos = pygame.Vector2(settings.START_POS)
        self.vel = pygame.Vector2()
        self.flying = False
        self.rest_time = 0.0
        self.accumulator = 0.0

    def launch_velocity(self, target):
        return (pygame.Vector2(target) - self.pos) * settings.LAUNCH_SCALE

    # --- loop --------------------------------------------------------
    def run(self):
        frame = 0
        while self.running:
            dt = min(self.clock.tick(settings.FPS) / 1000, 0.05)
            frame += 1
            if SMOKE_FRAMES:
                self._smoke_input(frame)
            for event in pygame.event.get():
                self.handle_event(event)
            self.update(dt)
            self.draw()
            pygame.display.flip()
        pygame.quit()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.key == pygame.K_r:
                self.reset()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.flying:
            self.vel = self.launch_velocity(event.pos)
            self.flying = True

    def update(self, dt):
        if not self.flying:
            return
        self.accumulator += dt
        while self.accumulator >= settings.PHYSICS_STEP:
            self.accumulator -= settings.PHYSICS_STEP
            self.pos, self.vel, on_floor = step(self.pos, self.vel, settings.PHYSICS_STEP)
            if is_resting(self.vel, on_floor):
                self.vel.update(0, 0)
                self.rest_time += settings.PHYSICS_STEP
            else:
                self.rest_time = 0.0
        off_screen = not self.screen.get_rect().inflate(400, 2000).collidepoint(self.pos)
        if self.rest_time >= settings.RESET_DELAY or off_screen:
            self.reset()

    def trajectory_preview(self, target):
        pos, vel = pygame.Vector2(self.pos), self.launch_velocity(target)
        dots = []
        steps = int(settings.PREVIEW_TIME / settings.PHYSICS_STEP)
        for i in range(1, steps + 1):
            pos, vel, on_floor = step(pos, vel, settings.PHYSICS_STEP)
            if i % settings.PREVIEW_DOT_EVERY == 0:
                dots.append((int(pos.x), int(pos.y)))
            if is_resting(vel, on_floor):
                break
        return dots

    def draw(self):
        screen = self.screen
        screen.fill(settings.BACKGROUND_COLOR)
        width, height = settings.SCREEN_SIZE
        pygame.draw.line(screen, settings.FLOOR_COLOR, (0, height - 1), (width, height - 1), 2)
        if not self.flying:
            mouse = pygame.mouse.get_pos()
            for dot in self.trajectory_preview(mouse):
                pygame.draw.circle(screen, settings.PREVIEW_COLOR, dot, 2)
            pygame.draw.aaline(screen, settings.AIM_COLOR, self.pos, mouse)
        pygame.draw.circle(screen, settings.BALL_COLOR, (int(self.pos.x), int(self.pos.y)), settings.BALL_RADIUS)
        screen.blit(self.hint, (10, 10))

    def _smoke_input(self, frame):
        if frame % 90 == 0:
            target = (100 + frame % 400, 100)
            pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=target, button=1))
            pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, pos=target, button=1))
        if frame % 300 == 0:
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r, mod=0, unicode="r", scancode=0))
        if frame >= SMOKE_FRAMES:
            self.running = False


if __name__ == "__main__":
    Demo().run()
