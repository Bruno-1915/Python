class part:
	def __init__(self, x, y, z, masa):
		self.x = x
		self.y = y
		self.z = z
		self.m = masa

	def __add__(self,other):
		m = self.m + other.m
		return part((self.x + other.x)/m, (self.y + other.y)/m, (self.z + other.z)/m, m)
	def __repr__(self):
		return "Posicion (" + str(self.x) + "i " + str(self.y) + "j " + str(self.z) + "k)  : Masa (" + str(self.m) + " )" 
