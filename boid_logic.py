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


class QuadTree:
    def __init__(self, nodes: List[QuadNode]):
        self.nodes = nodes
        
    def cleanup(self) -> None:
        to_process: List[int] = []
        if self.nodes[0].count == -1:
            to_process.append(0)

        while to_process:
            node_index: int = to_process.pop()
            node: QuadNode = self.nodes[node_index]

            num_empty_leaves: int = 0
            for j in range(4):
                child_index: int = node.first_child + j
                child: QuadNode = self.nodes[child_index]

                if child.count == 0:
                    num_empty_leaves += 1
                elif child.count == -1:
                    to_process.append(child_index)

            if num_empty_leaves == 4:
                self.nodes[node.first_child].first_child = self.free_node
                self.free_node = node.first_child

                node.first_child = -1
                node.count = 0


class QuadNode:
    def __init__(self, first_child: int, count: int):
        self.first_child = first_child
        self.count = count


class QuadNodeData:
    def __init__(self, index: int, crect: Tuple[int, int, int, int], depth: int):
        self.index = index
        self.crect = crect
        self.depth = depth


def child_data(
    mx: int, my: int, hx: int, hy: int, index: int, depth: int
) -> QuadNodeData:
    return QuadNodeData(index, (mx, my, hx, hy), depth)


def find_leaves(
    tree: QuadTree, root: QuadNodeData, rect: Tuple[int, int, int, int]
) -> List[QuadNodeData]:
    leaves = []
    to_process = [root]

    while len(to_process) > 0:
        nd = to_process.pop()

        if tree.nodes[nd.index] != -1:
            leaves.push(nd)
        else:
            mx = nd.crect[0]
            my = nd.crect[1]
            hx = nd.crect[2] // 2
            hy = nd.crect[3] // 2

            l = mx - hx
            t = my - hx
            r = mx + hx
            b = my + hy

            if rect[1] <= my:
                if rect[0] <= mx:
                    to_process.append(child_data(l, t, hx, hy, fc + 0, nd.depth + 1))
                if rect[2] > mx:
                    to_process.append(child_data(r, t, hx, hy, fc + 1, nd.depth + 1))
                if rect[3] > my:
                    if rect[0] <= mx:
                        to_process.append(
                            child_data(l, b, hx, hy, fc + 2, nd.depth + 1)
                        )
                if rect[2] > mx:
                    to_process.append(child_data(r, b, hx, hy, fc + 3, nd.depth + 1))

    return leaves




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
    count = 0
    for boid in boids:
        if boid != b and abs(boid.position - b.position) < 50:
            center_of_mass += boid.position
            count += 1
    if count:
        center_of_mass /= count
        return (center_of_mass - b.position) / 100
    return Vector(0, 0)


def rule2(b: Boid) -> Vector:
    c = Vector(0, 0)
    for boid in boids:
        if boid != b:
            distance = abs(boid.position - b.position)
            if distance < BOID_SEPARATION_RADIUS:
                c -= (boid.position - b.position) / distance
    return c * 0.5


def rule3(b: Boid) -> Vector:
    pv = Vector(0, 0)
    count = 0
    for boid in boids:
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
