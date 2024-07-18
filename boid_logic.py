from random import randint
import pygame


# constants
WIDTH = 800
HEIGHT = 800
BOID_COUNT = 100
BOID_SIZE = 5
BOID_COLOR = (255, 255, 255)
BOID_ACCELERATION = 0.1
BOID_MAX_SPEED = 5
BOID_SEPARATION_RADIUS = 20


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


class Boid:
    def __init__(self, position: Vector, velocity: Vector):
        self.position = position
        self.velocity = velocity


boids = []

boids.extend(
    [
        Boid(
            Vector(randint(0, 500), randint(0, 500)),
            Vector(randint(0, 500), randint(0, 500)),
        )
        for i in range(BOID_COUNT)
    ]
)


def draw_boids(screen) -> None:
    for b in boids:
        pygame.draw.circle(screen, (255, 255, 255), (b.position.x, b.position.y), 5)
    pygame.display.flip()


def move_all_boids_to_new_positions() -> None:
    v1: Vector
    v2: Vector
    v3: Vector

    for b in boids:
        v1 = rule1(b)
        v2 = rule2(b)
        v3 = rule3(b)

        b.velocity = b.velocity + v1 + v2 + v3
        limit_velocity(b)
        b.position = b.position + b.velocity
        bound_position(b)


def rule1(b: Boid) -> Vector:
    center_of_mass = Vector(0, 0)
    for boid in boids:
        if boid != b:
            center_of_mass += boid.position
    center_of_mass /= len(boids) - 1
    return (center_of_mass - b.position) / 100


def rule2(b: Boid) -> Vector:
    c = Vector(0, 0)
    for boid in boids:
        if boid != b:
            if abs(boid.position - b.position) < BOID_SEPARATION_RADIUS:
                c -= boid.position - b.position
    return c


def rule3(b: Boid) -> Vector:
    pv = Vector(0, 0)
    for boid in boids:
        if boid != b:
            pv += boid.velocity

    pv /= len(boids) - 1
    return (pv - b.velocity) / 8


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
    screen = pygame.display.set_mode((800, 800))
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
