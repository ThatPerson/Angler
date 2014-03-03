import math

def reduce_to(value, below):
	while (value > below):
		value = value - below
	return value



class Position:
	x = 0;
	y = 0;
	def __init__(self, x, y):
		self.x = x;
		self.y = y;

	def translate(self, angle, distance):
		angle = reduce_to(angle, 360)
		lateral_x = distance * math.cos(reduce_to(angle, 90))
		lateral_y = distance * math.sin(reduce_to(angle, 90))

		if (angle < 90):
			a = 1
		elif (angle < 180):
			# 2nd quadrant, y is negative
			lateral_y = -(lateral_y)
		elif (angle < 270):
			# 3rd, y and x negative
			lateral_y = -(lateral_y)
			lateral_x = -(lateral_x)
		elif (angle < 360):
			lateral_x = -(lateral_x)

		self.x = self.x + lateral_x
		self.y = self.y + lateral_y
	
	def to_string(self):
		return "X: "+str(self.x)+"\nY: "+str(self.y)
		

class Vector:
	magnitude = 0;
	direction = 0;
	def __init__(self, magnitude, direction):
		self.magnitude = magnitude
		self.direction = direction

	def to_string(self):
		return "Mag: "+str(self.magnitude)+"\nAngle: "+str(self.direction)

	def to_components(self):
		angle = reduce_to(self.direction, 360)
		angle_l = reduce_to(self.direction, 90)
		
		x = 0
		y = 0
		
		if (angle < 0):
			angle = angle + 360
		
		if (angle >= 0 and angle <= 90):
			x = self.magnitude * math.sin(angle_l)
			y = self.magnitude * math.cos(angle_l)
		elif (angle >= 90 and angle <= 180):
			x = self.magnitude * math.cos(angle_l)
			y = -(self.magnitude * math.sin(angle_l))
		elif (angle >= 180 and angle <= 270):
			x = -(self.magnitude * math.sin(angle_l))
			y = -(self.magnitude * math.cos(angle_l))
		elif (angle >= 270):
			x = -(self.magnitude * math.cos(angle_l))
			y = self.magnutide * math.sin(angle_l)
		
		return Position(x, y)		

def balance_vectors(vectors):
	total = Position(0, 0)
	po = Position(0, 0)
	for i in range(0, len(vectors)):
		po = vectors[i].to_components()
		print(po.to_string())
		total.x += po.x
		total.y += po.y
	l = Vector(0, 0)
	l.magnitude = math.sqrt((total.x*total.x)+(total.y*total.y))
	l.direction = math.atan2(total.y, total.x)
	if (l.direction < 0.001):
		l.direction = 0;
	if (l.magnitude < 0.001):
		l.magnitude = 0;
	return l

class Particle:
	position = Position(0,0)
	forces = []
	tmp_forces = []
	motion = Vector(0,0)
	name = ""
	mass = 0
	def __init__(self, forces, position, tmp_forces, name, mass, motion):
		self.position = position
		self.forces = forces
		self.tmp_forces = tmp_forces
		self.name = name
		self.mass = mass
		self.motion = motion
		
	def to_string(self):
		stri =  "Name: "+self.name+"\nMass: "+str(self.mass)+"\nPosition: \n"+self.position.to_string()
		for i in range(0, len(self.forces)):
			stri += "\nForce:\n"+self.forces[i].to_string()
		for i in range(0, len(self.tmp_forces)):
			stri += "\nTMP Force:\n"+self.tmp_forces[i].to_string()
		return stri
	def wait(self, time):
		force = balance_vectors(self.forces)
		forcer = balance_vectors(self.tmp_forces)
		force = balance_vectors([force, forcer])
		force.magnitude = force.magnitude * time
		motion = balance_vectors([force, self.motion])
		quop = self.motion.to_components()
		self.position.x += quop.x
		self.position.y += quop.y
		self.tmp_forces = []


vec = Vector(2, (0))
par = Particle([vec], Position(10, 5), [], "Mars", 10, Vector(2, 0))
#print(par.to_string())

vect = Vector(2, (math.pi*5/4))

l = balance_vectors([vec, vect])
print(l.to_string())

par.wait(1)
print(par.to_string())
