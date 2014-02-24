def reduce_to(value, below):
	while (value > below):
		value = value - below
	return value

class Position:
	x;
	y;
	def __init__(self, x, y):
		self.x = x;
		self.y = y;

	def translate(self, angle, distance):
		angle = reduce_to(angle, 360)
		lateral_x = distance * cos(reduce_to(angle, 90))
		lateral_y = distance * sin(reduce_to(angle, 90))

		if (angle < 90):
			# do nothing
		else if (angle < 180):
			# 2nd quadrant, y is negative
			lateral_y = -(lateral_y)
		else if (angle < 270):
			# 3rd, y and x negative
			lateral_y = -(lateral_y)
			lateral_x = -(lateral_x)
		else if (angle < 360):
			lateral_x = -(lateral_x)

		self.x = self.x + lateral_x
		self.y = self.y + lateral_y

class Vector:
	magnitude;
	direction;
	def __init__(self, magnitude, direction):
		self.magnitude = magnitude
		self.direction = direction

	def to_components(self):
		


class Particle:
	position;
