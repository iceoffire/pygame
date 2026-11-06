"""Paint: pick a color from the RGB bars and paint on a canvas."""
import os
import sys
from datetime import datetime

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


def make_bar(channel):
    """Vertical gradient for one color channel (0=red, 1=green, 2=blue): 255 at the top, 0 at the bottom."""
    bar = pygame.Surface((settings.BAR_WIDTH, settings.BAR_HEIGHT))
    for row in range(settings.BAR_HEIGHT):
        color = [0, 0, 0]
        color[channel] = bar_value(row)
        pygame.draw.line(bar, color, (0, row), (settings.BAR_WIDTH - 1, row))
    return bar


def bar_value(row):
    """Channel value for a row inside a bar (row 0 = 255, last row = 0)."""
    row = max(0, min(settings.BAR_HEIGHT - 1, row))
    return 255 - int(255 * row / (settings.BAR_HEIGHT - 1))


def bar_row(value):
    return int((255 - value) * (settings.BAR_HEIGHT - 1) / 255)


class Demo:
    def __init__(self):
        require_pygame_ce()
        pygame.init()
        flags = 0 if os.environ.get("SDL_VIDEODRIVER") == "dummy" else pygame.SCALED
        self.screen = pygame.display.set_mode(settings.SCREEN_SIZE, flags)
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, settings.FONT_SIZE)

        width, height = settings.SCREEN_SIZE
        self.canvas = pygame.Surface((width - settings.PANEL_WIDTH, height)).convert()
        self.canvas_pos = (settings.PANEL_WIDTH, 0)
        self.canvas.fill(settings.CANVAS_COLOR)

        self.bars = [make_bar(channel) for channel in range(3)]
        self.bar_rects = [pygame.Rect(x, settings.BAR_TOP, settings.BAR_WIDTH, settings.BAR_HEIGHT)
                          for x in settings.BAR_XS]
        self.help_lines = [self.font.render(line, True, settings.TEXT_COLOR)
                           for line in ("Click bars:", "  pick color", "Wheel: size", "S: save", "X: clear", "Esc: quit")]

        self.color = list(settings.START_COLOR)
        self.brush_size = settings.BRUSH_SIZE
        self.dragging_bar = None   # index of the bar being dragged, if any
        self.last_point = None     # last canvas point of the current stroke
        self.message = ""
        self.message_time = 0.0
        self.running = True

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
            self.message_time = max(0.0, self.message_time - dt)
            self.draw()
            pygame.display.flip()
        pygame.quit()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.key == pygame.K_x:
                self.canvas.fill(settings.CANVAS_COLOR)
            elif event.key == pygame.K_s:
                self.save()
        elif event.type == pygame.MOUSEWHEEL:
            self.brush_size = max(settings.BRUSH_SIZE_MIN, min(settings.BRUSH_SIZE_MAX, self.brush_size + event.y))
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.press(event.pos)
        elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
            self.drag(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging_bar = None
            self.last_point = None

    def to_canvas(self, pos):
        return (pos[0] - self.canvas_pos[0], pos[1] - self.canvas_pos[1])

    def press(self, pos):
        for i, rect in enumerate(self.bar_rects):
            if rect.collidepoint(pos):
                self.dragging_bar = i
                self.pick(pos)
                return
        if pos[0] >= settings.PANEL_WIDTH:
            self.last_point = self.to_canvas(pos)
            self.paint(self.last_point, self.last_point)

    def drag(self, pos):
        if self.dragging_bar is not None:
            self.pick(pos)
        elif self.last_point is not None:
            point = self.to_canvas(pos)
            self.paint(self.last_point, point)
            self.last_point = point

    def pick(self, pos):
        self.color[self.dragging_bar] = bar_value(pos[1] - settings.BAR_TOP)

    def paint(self, start, end):
        """Line between two mouse samples plus round caps, so fast strokes have no gaps."""
        if start != end:
            pygame.draw.line(self.canvas, self.color, start, end, self.brush_size * 2)
        pygame.draw.circle(self.canvas, self.color, start, self.brush_size)
        pygame.draw.circle(self.canvas, self.color, end, self.brush_size)

    def save(self):
        path = settings.SAVE_DIR / f"painting_{datetime.now():%Y%m%d_%H%M%S}.png"
        pygame.image.save(self.canvas, str(path))
        self.message = f"Saved {path.name}"
        self.message_time = settings.MESSAGE_TIME

    # --- drawing -----------------------------------------------------
    def draw(self):
        screen = self.screen
        screen.blit(self.canvas, self.canvas_pos)
        self.draw_brush_cursor()
        self.draw_panel()
        if self.message_time > 0:
            text = self.font.render(self.message, True, settings.TEXT_COLOR, settings.PANEL_COLOR)
            screen.blit(text, (settings.PANEL_WIDTH + 8, 8))

    def draw_brush_cursor(self):
        pos = pygame.mouse.get_pos()
        if pos[0] >= settings.PANEL_WIDTH + self.brush_size:
            pygame.draw.circle(self.screen, (128, 128, 128), pos, self.brush_size, 1)

    def draw_panel(self):
        screen = self.screen
        screen.fill(settings.PANEL_COLOR, (0, 0, settings.PANEL_WIDTH, settings.SCREEN_SIZE[1]))
        screen.blit(self.font.render("Color", True, settings.TEXT_COLOR), (14, 14))
        for channel, (bar, rect) in enumerate(zip(self.bars, self.bar_rects)):
            screen.blit(bar, rect)
            pygame.draw.rect(screen, settings.BAR_OUTLINE, rect.inflate(2, 2), 1)
            y = rect.top + bar_row(self.color[channel])
            # Marker: a small triangle pointing at the current value, left of the bar.
            pygame.draw.polygon(screen, settings.MARKER_COLOR,
                                [(rect.left - 2, y), (rect.left - 8, y - 4), (rect.left - 8, y + 4)])

        swatch = pygame.Rect(settings.SWATCH_RECT)
        pygame.draw.rect(screen, self.color, swatch)
        pygame.draw.rect(screen, settings.BAR_OUTLINE, swatch, 1)

        y = swatch.bottom + 8
        screen.blit(self.font.render(f"Size: {self.brush_size}", True, settings.TEXT_COLOR), (14, y))
        y += 24
        for line in self.help_lines:
            screen.blit(line, (8, y))
            y += 18

    def _smoke_input(self, frame):
        # Scripted strokes, color picks, wheel and clear. S (save) is skipped so no file is written.
        cycle = frame % 120
        if cycle == 10:
            pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(200, 200), button=1))
        elif 10 < cycle < 40:
            pos = (200 + (cycle - 10) * 15, 200 + (cycle - 10) * 5)
            pygame.event.post(pygame.event.Event(pygame.MOUSEMOTION, pos=pos, rel=(15, 5), buttons=(1, 0, 0)))
        elif cycle == 40:
            pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, pos=(650, 350), button=1))
        elif cycle == 50:
            bar = self.bar_rects[(frame // 120) % 3]
            pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=bar.center, button=1))
            pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, pos=bar.center, button=1))
        elif cycle == 60:
            pygame.event.post(pygame.event.Event(pygame.MOUSEWHEEL, x=0, y=2, flipped=False,
                                                 precise_x=0.0, precise_y=2.0))
        if frame % 600 == 0:
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_x, mod=0, unicode="x", scancode=0))
        if frame >= SMOKE_FRAMES:
            self.running = False


if __name__ == "__main__":
    Demo().run()
