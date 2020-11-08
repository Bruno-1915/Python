class Vec2:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def __add__(self,other):
		print(self,' + ',other)
		return Vec2(self.x + other.x, self.y + other.y, self.z + other.z)
	def __sub__(self,other):
		return Vec2(self.x - other.x, self.y - other.y, self.z - other.z)
	def __mul__(self,other):
		return Vec2(self.x * other.x, self.y * other.y, self.z * other.z)
	def __xor__(self,other):
		return Vec2((self.y * other.z) - (self.z * other.y), (self.z * other.x) - (self.x * other.z), (self.x * other.y) - (self.y * other.x))	
	def __mag__(self):
		return ((self.x * self.x) + (self.y * self.y) + (self.z * self.z))**0.5
	def __repr__(self):
		return "( " + str(self.x) + "i " + str(self.y) + "j " + str(self.z) + "k " + ")"

