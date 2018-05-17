import Collider2D_AABB, pygame, Animation

class Sprite():
    all_Sprites = []
    def __init__(self, x, y, path, collider=False, animation=None, scale=1):
        self.x = x
        self.y = y
        self.img = pygame.image.load(path)
        if scale != 1:
            self.img = pygame.transform.scale(self.img, (self.img.get_width()*scale, self.img.get_height()*scale))
        self.width = width
        self.height = height
        if collider != False:
            Collider2D_AABB(self, (collider['x'], collider['y']), collider['width'], collider['height'])
            self.is_grounded = False
            self.x_speed = 0
            self.y_speed = 0
            self.collider = True
        if animation!=None:
            self.animation = Animation(animation[0], animation[1])
        self.all_Sprites.append(self)
    
    def __call__():
        return all_Sprites
        def update_move():
            print('o')

    def teleport(self, (x, y)):
        self.x = x
        self.y = y