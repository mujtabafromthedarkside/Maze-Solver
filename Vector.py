import math
import random

# A 2-dimensional Vector
class Vector:
    def __init__(self):
        self.x = 0
        self.y = 0

    # Constructor, takes the components of Vector as input
    def __init__(self, x , y):
        self.x = x
        self.y = y

    # returns sum of 2 Vectors
    def add(u, v):
        return Vector(u.x + v.x, u.y + v.y)

    # adds in-place
    def add(self, v):
        self.x += v.x
        self.y += v.y

    # ensures unary - operator works with a Vector
    def __neg__(self):
        return Vector(-self.x, -self.y)

    # Given an angle, returns the unit Vector for that angle.
    def fromAngle(angle):
        return Vector(math.cos(angle), math.sin(angle))

    # Limits the magnitude of the Vector
    def limit(self, mx):
        mg = self.mag()
        if mg > mx:
            self.normalize()
            self.x *= mx
            self.y *= mx

    # makes magnitude = 1 without affect direction
    def normalize(self):
        mg = self.mag()
        self.x /= mg
        self.y /= mg

    # returns magnitude of a Vector
    def mag(self):
        return math.sqrt(self.x**2 + self.y**2)

    # returns distance between 2 Vectors
    def dist(a,b, x,y):
        return math.sqrt((x-a)**2 + (y-b)**2)

    # ensures print(Vector) works
    def __str__(self):
        return str(self.x) + ' ' + str(self.y)

    # returns a copy of the Vector
    def copy(self):
        return Vector(self.x, self.y)

    # returns a random unit Vector
    def random_dir():
        rnd = random.randint(0, 360)
        return Vector.fromAngle(rnd)