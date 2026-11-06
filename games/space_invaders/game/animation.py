"""Frame-based animation driven by dt. Frames come from the assets cache, never from disk."""


class Animation:
    def __init__(self, frames, frame_time, loop=True, start=0):
        self.frames = frames
        self.frame_time = frame_time
        self.loop = loop
        self.index = start % len(frames)
        self.time = 0.0
        self.finished = False

    @property
    def image(self):
        return self.frames[self.index]

    def update(self, dt):
        if self.finished:
            return
        self.time += dt
        while self.time >= self.frame_time:
            self.time -= self.frame_time
            if self.index + 1 < len(self.frames):
                self.index += 1
            elif self.loop:
                self.index = 0
            else:
                self.finished = True
                return
