"""OpenGL 3D: a textured cube you can rotate, move and zoom (pygame window + PyOpenGL)."""
import os
import sys

import pygame

import settings

try:
    from OpenGL.GL import (
        GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST, GL_LINEAR, GL_MODELVIEW,
        GL_PROJECTION, GL_QUADS, GL_RGBA, GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
        GL_TEXTURE_MIN_FILTER, GL_UNPACK_ALIGNMENT, GL_UNSIGNED_BYTE,
        glBegin, glBindTexture, glClear, glDeleteTextures, glDisable, glEnable, glEnd,
        glGenTextures, glLoadIdentity, glMatrixMode, glPixelStorei, glRotatef, glTexCoord2fv,
        glTexImage2D, glTexParameteri, glTranslatef, glVertex3fv,
    )
    from OpenGL.GLU import gluPerspective
except ImportError:
    sys.exit("This demo needs PyOpenGL. Fix: pip install -r requirements.txt")

# Smoke-test hooks (see tools/smoke_test.py, which skips this demo). Unset in normal use.
SMOKE_FRAMES = int(os.environ.get("SMOKE_FRAMES", "0"))
SMOKE_KEYS = (pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_r, pygame.K_f, pygame.K_LEFT, pygame.K_UP)


def require_pygame_ce():
    if not getattr(pygame, "IS_CE", False):
        sys.exit(
            "This project needs pygame-ce, but the classic 'pygame' package is installed.\n"
            "Fix: pip uninstall pygame && pip install -r requirements.txt"
        )


def load_texture(path):
    """Upload an image file as an OpenGL texture and return its id."""
    surface = pygame.image.load(path)
    data = pygame.image.tobytes(surface, "RGBA", True)  # flipped: OpenGL's origin is bottom-left
    width, height = surface.get_size()
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    return texture_id


class Cube:
    VERTICES = (
        (1, -1, -1), (1, -1, 1), (-1, -1, 1), (-1, -1, -1),
        (1, 1, -1), (1, 1, 1), (-1, 1, 1), (-1, 1, -1),
    )
    FACES = (  # indices into VERTICES
        (0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1),
        (1, 5, 6, 2), (2, 6, 7, 3), (4, 0, 3, 7),
    )
    TEX_COORDS = ((0, 0), (1, 0), (1, 1), (0, 1))

    def __init__(self, texture_path):
        self.rotation = [0.0, 0.0, 0.0]   # degrees around X, Y, Z
        self.x = 0.0
        self.y = 0.0
        self.distance = 0.0               # 0 = start distance; negative = farther away
        self.texture_id = load_texture(texture_path)

    def update(self, keys, dt):
        turn = settings.ROTATE_SPEED * dt
        move = settings.MOVE_SPEED * dt
        for axis, key in enumerate((pygame.K_a, pygame.K_s, pygame.K_d)):
            if keys[key]:
                self.rotation[axis] = (self.rotation[axis] + turn) % 360
        if keys[pygame.K_r]:
            self.distance -= move
        if keys[pygame.K_f]:
            self.distance = min(0.0, self.distance + move)
        self.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * move
        self.y += (keys[pygame.K_UP] - keys[pygame.K_DOWN]) * move

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(self.x, self.y, settings.START_DISTANCE + self.distance)
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glBegin(GL_QUADS)
        for face in self.FACES:
            for corner, vertex in enumerate(face):
                glTexCoord2fv(self.TEX_COORDS[corner])
                glVertex3fv(self.VERTICES[vertex])
        glEnd()
        glDisable(GL_TEXTURE_2D)

    def delete(self):
        glDeleteTextures([self.texture_id])


class Demo:
    def __init__(self):
        require_pygame_ce()
        pygame.init()
        # pygame.SCALED can't be combined with OPENGL, so the window is created at its real size.
        pygame.display.set_mode(settings.SCREEN_SIZE, pygame.DOUBLEBUF | pygame.OPENGL)
        pygame.display.set_caption(f"{settings.TITLE}  |  {settings.CONTROLS}")
        self.clock = pygame.time.Clock()

        width, height = settings.SCREEN_SIZE
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(settings.FIELD_OF_VIEW, width / height, settings.NEAR_PLANE, settings.FAR_PLANE)
        glEnable(GL_DEPTH_TEST)

        self.cube = Cube(settings.TEXTURE)
        self.running = True

    def run(self):
        frame = 0
        while self.running:
            dt = min(self.clock.tick(settings.FPS) / 1000, 0.05)
            frame += 1
            if SMOKE_FRAMES:
                self._smoke_input(frame)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
            self.cube.update(pygame.key.get_pressed(), dt)
            self.cube.render()
            pygame.display.flip()
        self.cube.delete()
        pygame.quit()

    def _smoke_input(self, frame):
        # Held keys are read with key.get_pressed(), so posted events only check the event path.
        if frame % 30 == 0:
            key = SMOKE_KEYS[(frame // 30) % len(SMOKE_KEYS)]
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=key, mod=0, unicode="", scancode=0))
            pygame.event.post(pygame.event.Event(pygame.KEYUP, key=key, mod=0, unicode="", scancode=0))
        if frame >= SMOKE_FRAMES:
            self.running = False


if __name__ == "__main__":
    Demo().run()
