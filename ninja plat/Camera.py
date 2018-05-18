class Camera():
    def __init__(self, (x, y)):
        self.x = x
        self.y = y
        self.bounds = (0, 0)

    def set_focus(self, (x, y), ignore_bounds=False):
        if abs(self.x-x)>2:
			self.x = self.x+(x-self.x)/10
		else:
			self.x = x
		if abs(y-self.y)>2:
			self.y = self.y+(y-self.y)/10
		else:
			self.y = y
        if not ignore_bounds:
			self.check_sides()
	def check_sides(self):
		if self.x<0:
			self.x = 0
		elif self.x>self.bounds[0]:
			self.x = self.bounds[0]
		if self.y<0:
			self.y = 0
		elif self.y>self.bounds[1]:
			self.y = self.bounds[1]
	