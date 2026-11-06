"""Frame-based animation. Holds only names and timing; the images come from the assets cache."""


class Animation:
    def __init__(self, pattern, clips, start):
        """
        pattern: path with {name} and {index} fields, e.g. "images/player/{name}_{index:02d}.png"
        clips:   name -> (frame count, seconds per frame)
        """
        self.pattern = pattern
        self.clips = clips
        self.name = start
        self.index = 0
        self.time = 0.0

    def play(self, name):
        """Switch clip (restarting it); does nothing if it's already playing."""
        if name != self.name:
            self.name = name
            self.index = 0
            self.time = 0.0

    def update(self, dt):
        count, frame_time = self.clips[self.name]
        self.time += dt
        while self.time >= frame_time:
            self.time -= frame_time
            self.index = (self.index + 1) % count

    @property
    def frame_name(self):
        return self.pattern.format(name=self.name, index=self.index)

    def all_frame_names(self):
        for name, (count, _) in self.clips.items():
            for index in range(count):
                yield self.pattern.format(name=name, index=index)
