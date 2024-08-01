from random import randint, uniform
import pygame
import math


# constants
WIDTH = 1200
HEIGHT = 800
BOID_COUNT = 100
BOID_SIZE = 5
BOID_COLOR = (255, 255, 255)
BOID_ACCELERATION = 0.1
BOID_MAX_SPEED = 10
BOID_SEPARATION_RADIUS = 30


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other) -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other) -> "Vector":
        return Vector(self.x - other.x, self.y - other.y)

    def __truediv__(self, other) -> "Vector":
        return Vector(self.x / other, self.y / other)

    def __mul__(self, other) -> "Vector":
        return Vector(self.x * other, self.y * other)

    def __abs__(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def normalize(self) -> "Vector":
        magnitude = abs(self)
        if magnitude == 0:
            return Vector(0, 0)
        return self / magnitude

    def dot(self, other) -> float:
        return self.x * other.x + self.y * other.y


class Node:
    def __init__(self, position: Vector):
        self.position = position
        self.boids = []


class QuadTree:
    def __init__(self, topL, botR, capacity=12):
        self.topL = topL
        self.botR = botR
        self.children = None
        self.topLeftTree = None
        self.topRightTree = None
        self.botLeftTree = None
        self.botRightTree = None
        self.divided = False
        self.capacity = capacity
        self.nodes = []

    def insert(self, node: Node):
        if not self.inBoundary(node.position):
            return False

        if len(self.nodes) < self.capacity:
            self.nodes.append(node)
            return True

        if not self.divided
            self.subdivide()
            

        if abs(self.topL.x - self.botR.x) <= 1 and abs(self.topL.y - self.botR.y) <= 1:
            if self.children is None:
                self.children = []
            return

        if (self.topL.x + self.botR.x) / 2 >= node.position.x:
            if (self.topL.y + self.botR.y) / 2 >= node.position.y:
                if self.topLeftTree is None:
                    self.topLeftTree = QuadTree(
                        self.topL,
                        Vector(
                            (self.topL.x + self.botR.x) / 2,
                            (self.topL.y + self.botR.y) / 2,
                        ),
                    )
                self.topLeftTree.insert(node)
            else:
                if self.botLeftTree is None:
                    self.botLeftTree = QuadTree(
                        Vector(self.topL.x, (self.topL.y + self.botR.y) / 2),
                        Vector((self.topL.x + self.botR.x) / 2, self.botR.y),
                    )
                self.botLeftTree.insert(node)

        else:
            if (self.topL.y + self.botR.y) / 2 >= node.position.y:
                if self.topRightTree is None:
                    self.topRightTree = QuadTree(
                        Vector((self.topL.x + self.botR.x) / 2, self.topL.y),
                        Vector(self.botR.x, (self.topL.y + self.botR.y) / 2),
                    )
                self.topRightTree.insert(node)
            else:
                if self.botRightTree is None:
                    self.botRightTree = QuadTree(
                        Vector(
                            (self.topL.x + self.botR.x) / 2,
                            (self.topL.y + self.botR.y) / 2,
                        ),
                        self.botR,
                    )
                self.botRightTree.insert(node)
                
    def subdivide(self):
        self.divided = True
        self.topLeftTree = QuadTree(
            self.topL,
            Vector((self.topL.x + self.botR.x) / 2, (self.topL.y + self.botR.y) / 2),
        )
        self.topRightTree = QuadTree(
            Vector((self.topL.x + self.botR.x) / 2, self.topL.y),
            Vector(self.botR.x, (self.topL.y + self.botR.y) / 2),
        )
        self.botLeftTree = QuadTree(
            Vector(self.topL.x, (self.topL.y + self.botR.y) / 2),
            Vector((self.topL.x + self.botR.x) / 2, self.botR.y),
        )
        self.botRightTree = QuadTree(
            Vector((self.topL.x + self.botR.x) / 2, (self.topL.y + self.botR.y) / 2),
            self.botR,
        )
        

    def search(self, range):
        found = []
        if not self.intersects(range):
            return found
        for node in self.nodes:
            if range.contains(node.position):
                found.append(node)
        if not self.divided:
            return found
        found.extend(self.topLeftTree.search(range))
        found.extend(self.topRightTree.search(range))
        found.extend(self.botLeftTree.search(range))
        found.extend(self.botRightTree.search(range))
        return found

    def intersects(self, range):
        return not (
            range.topL.x > self.botR.x
            or range.botR.x < self.topL.x
            or range.topL.y > self.botR.y
            or range.botR.y < self.topL.y
        )

    def contains(self, position: Vector):
        return (
            position.x >= self.topL.x
            and position.x <= self.botR.x
            and position.y >= self.topL.y
            and position.y <= self.botR.y
        )

    def inBoundary(self, position: Vector):
        return (
            position.x >= self.topL.x
            and position.x <= self.botR.x
            and position.y >= self.topL.y
            and position.y <= self.botR.y
        )


class Boid:
    def __init__(self, position: Vector, velocity: Vector):
        self.position = position
        self.velocity = velocity


boids = []

boids.extend(
    [
        Boid(
            Vector(randint(0, WIDTH), randint(0, HEIGHT)),
            Vector(uniform(-1, 1) * 10, uniform(-1, 1) * 10),
        )
        for i in range(BOID_COUNT)
    ]
)

quad_tree = QuadTree(Vector(0, 0), Vector(WIDTH, HEIGHT))

for b in boids:
    quad_tree.insert(Node(b.position))


def draw_boids(screen) -> None:
    for b in boids:
        angle = math.atan2(b.velocity.y, b.velocity.x)
        cos_theta = math.cos(angle)
        sin_theta = math.sin(angle)

        # Define the points of the triangle relative to the boid's position
        p1 = (b.position.x, b.position.y)
        p2 = (
            b.position.x - 10 * cos_theta + 5 * sin_theta,
            b.position.y - 10 * sin_theta - 5 * cos_theta,
        )
        p3 = (
            b.position.x - 10 * cos_theta - 5 * sin_theta,
            b.position.y - 10 * sin_theta + 5 * cos_theta,
        )

        # Draw the triangle
        pygame.draw.polygon(screen, BOID_COLOR, [p1, p2, p3])
    pygame.display.flip()


def move_all_boids_to_new_positions() -> None:
    v1: Vector
    v2: Vector
    v3: Vector

    global quad_tree
    quad_tree = QuadTree(Vector(0, 0), Vector(WIDTH, HEIGHT))

    for b in boids:
        v1 = rule1(b)
        v2 = rule2(b)
        v3 = rule3(b)

        b.velocity = b.velocity + v1 + v2 + v3
        limit_velocity(b)
        b.position = b.position + b.velocity
        bound_position(b)

        quad_tree.insert(Node(b.position))


def get_nearby_boids(b: Boid, radius: float) -> list[Boid]:

    search_area = QuadTree(
        Vector(b.position.x - radius, b.position.y - radius),
        Vector(b.position.x + radius, b.position.y + radius),
    )
    nodes = quad_tree.search(search_area)

    return [boid for node in nodes for boid in node.boids if boid != b]


def rule1(b: Boid) -> Vector:
    center_of_mass = Vector(0, 0)
    count = 0
    nearby_boids = get_nearby_boids(b, 50)
    for boid in nearby_boids:
        if boid != b and abs(boid.position - b.position) < 50:
            center_of_mass += boid.position
            count += 1
    if count:
        center_of_mass /= count
        return (center_of_mass - b.position) / 100
    return Vector(0, 0)


def rule2(b: Boid) -> Vector:
    c = Vector(0, 0)
    nearby_boids = get_nearby_boids(b, 50)
    for boid in nearby_boids:
        if boid != b:
            distance = abs(boid.position - b.position)
            if distance < BOID_SEPARATION_RADIUS:
                c -= (boid.position - b.position) / distance
    return c * 0.5


def rule3(b: Boid) -> Vector:
    pv = Vector(0, 0)
    count = 0
    nearby_boids = get_nearby_boids(b, 100)
    for boid in nearby_boids:
        if boid != b and abs(boid.position - b.position) < 100:
            pv += boid.velocity
            count += 1
    if count:
        pv /= count
        return (pv - b.velocity) / 8
    return Vector(0, 0)


def limit_velocity(b: Boid) -> None:
    if abs(b.velocity) > BOID_MAX_SPEED:
        b.velocity = b.velocity / abs(b.velocity) * 5


def bound_position(b: Boid) -> None:
    if b.position.x < 0:
        b.position.x = WIDTH
    elif b.position.x > WIDTH:
        b.position.x = 0
    if b.position.y < 0:
        b.position.y = HEIGHT
    elif b.position.y > HEIGHT:
        b.position.y = 0


def main():

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Boids")
    clock = pygame.time.Clock()
    running = True

    draw_boids(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        move_all_boids_to_new_positions()
        draw_boids(screen)
        clock.tick(30)


if __name__ == "__main__":
    main()
