from Random import randint

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other) -> 'Vector':
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other) -> 'Vector':
        return Vector(self.x - other.x, self.y - other.y)

    def __truediv__(self, other) -> 'Vector':
        return Vector(self.x / other, self.y / other)

    def __mul__(self, other) -> 'Vector':
        return Vector(self.x * other, self.y * other)

    def __abs__(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def __repr__(self) -> str:
        return f'({self.x}, {self.y})'

class Boid:
    def __init__(self, position:Vector, velocity:Vector):
        self.position = position
        self.velocity = velocity


boids = []

boids.append(Boid(Vector(randint(0, 100), randint(0, 100)), Vector(randint(0, 100), randint(0, 100))) for i in range(50))



"""
initialize positions of boids
LOOP
    draw boids()
    move all boids to new positions()
END LOOP
"""


def draw_boids() -> None:
    pass


def move_all_boids_to_new_positions() -> None:
    v1: Vector
    v2: Vector
    v3: Vector
    
    for b in boids:
        v1 = rule1(b)
        v2 = rule2(b)
        v3 = rule3(b)

        b.velocity = b.velocity + v1 + v2 + v3
        b.position = b.position + b.velocity
    """
    vector v1, v2, v3
    Boid b
    for b in boids:
        v1 = rule1(b)
        v2 = rule2(b)
        v3 - rule3(b)

        b.velocity = b.velocity + v1 + v2 + v3
        b.position = b.position + b.velocity
    """

def rule1(b: Boid) -> Vector:
    center_of_mass = 0
    count = 0
    for boid in boids:
        if boid != b:
            count += 1
            center_of_mass += boid.position
    if count:
        center_of_mass /= count
    return (center_of_mass - b.position) / 100

def rule2(b: Boid) -> Vector:
    c = 0
    for boid in boids:
        if boid != b:
            if abs(boid.position - b.position) < 100:
                c -= (boid.position - b.position)
    return c

def rule3(b: Boid) -> Vector:
    pv: Vector = 0
    for boid in boids:
        if boid != b:
            pv += boid.velocity
            
    pv /= len(boids) - 1
    return (pv - b.velocity) / 8
    

def main():
    pass
