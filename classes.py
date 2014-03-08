import math

G = 6.67*pow(10, -11)

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
		angle = reduce_to(self.direction, (math.pi*2))
		angle_l = reduce_to(self.direction, (math.pi*2)/4)
		
		x = 0
		y = 0
		
		if (angle < 0):
			angle = angle + 360
		
		if (angle >= 0 and angle <= (math.pi*2)/4):
			x = self.magnitude * math.sin(angle_l)
			y = self.magnitude * math.cos(angle_l)
		elif (angle >= (math.pi*2)/4 and angle <= (math.pi*2)/2):
			x = self.magnitude * math.cos(angle_l)
			y = -(self.magnitude * math.sin(angle_l))
		elif (angle >= (math.pi*2)/2 and angle <= (3*(math.pi*2)/4)):
			x = -(self.magnitude * math.sin(angle_l))
			y = -(self.magnitude * math.cos(angle_l))
		elif (angle >= (3*(math.pi*2)/4)):
			x = -(self.magnitude * math.cos(angle_l))
			y = self.magnutide * math.sin(angle_l)
		
		return Position(x, y)		

def balance_vectors(vectors):
	
	total = Position(0, 0)
	po = Position(0, 0)
	for i in range(0, len(vectors)):
		po = vectors[i].to_components()
		total.x += po.x
		total.y += po.y
	l = Vector(0, 0)
	l.magnitude = math.sqrt((total.x*total.x)+(total.y*total.y))
	if (total.x == 0 and total.y >= 0):
		l.direction = 0
	elif (total.y < 0):
		l.direction = math.pi
	else:
		l.direction = math.atan(total.y/total.x)

	if (total.x >= 0 and total.y >= 0):
		total.x = total.x
	elif (total.x >= 0 and total.y < 0):
		l.direction = total.direction + (math.pi)/2
	elif (total.x < 0 and total.y < 0):
		l.direction = total.direction + (math.pi)
	elif (total.x < 0 and total.y >= 0):
		l.direction = total.direction + (math.pi) + (math.pi/2)

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
		#forcer = balance_vectors(self.tmp_forces)
		#force = balance_vectors([force, forcer])

		force.magnitude = force.magnitude * time
		self.motion = balance_vectors([force, self.motion])

		quop = self.motion.to_components()
		self.position.x += quop.x
		self.position.y += quop.y
		self.tmp_forces = []

	def to_csv(self):
		return self.name+","+str(self.position.x)+","+str(self.position.y)

	def reset(self):
		self.tmp_forces = []
		return

	def get_grav(self, particle):
		F = GM/r^2
		mag = ((self.position.y - particle.position.y)*(self.position.y - particle.position.y)) + ((self.position.x - particle.position.x)*(self.position.x - particle.position.x))
		force = (G*particle.mass)/mag
		direction = (math.pi/2) - atan2(particle.position.y-self.position.y, particle.position.x-self.position.x)
		return Vector(force, direction)

vec = Vector(2, (0))
par = Particle([Vector(20, 0), Vector(2, 0)], Position(10, 5), [], "Mars", 10, Vector(1,(math.pi/2)))
#print(par.to_string())

vect = Vector(2, (math.pi*5/4))



print("Name\tX\tY")

for i in range (0, 100):
	print(par.to_csv())
	par.wait(1)
