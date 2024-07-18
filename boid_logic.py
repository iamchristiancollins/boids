"""
initialize positions of boids
LOOP
    draw boids()
    move all boids to new positions()
END LOOP
"""


def draw_boids():
    pass


def move_all_boids_to_new_positions():
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
    pass

def rule1(b: Boid):
    center_of_mass = 0
    count = 0
    for boid in boids:
        if boid != b:
            count += 1
            center_of_mass += boid.position
    if count:
        center_of_mass /= count
    return (center_of_mass - b.position) / 100

def main():
    pass
