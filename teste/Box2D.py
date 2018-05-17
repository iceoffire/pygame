class Box2D:
    all = []
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.all.append(self)
    
    @staticmethod
    def move():
        for gO in all:
            gO.x += 0.1