from types import SimpleNamespace
import random
import math
import sys

# ST_INIT = time.time()

DEPTH = 3
MY_MOVE_RANGE = 1000
MY_MOVE_RANGE_SQUARE = MY_MOVE_RANGE * MY_MOVE_RANGE
ZOMBIE_MOVE_RANGE = 400
ZOMBIE_MOVE_RANGE_SQUARE = ZOMBIE_MOVE_RANGE * ZOMBIE_MOVE_RANGE
MY_KILL_RANGE_SQUARE = 4000000
ZOMBIE_KILL_RANGE_SQUARE = 160000
GENERATOR_RANGE = 3000
FIB = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377,
       610, 987, 1597, 2584, 4181, 6765, 10946, 17711,
       28657, 46368, 75025, 121393, 196418, 317811, 514229]

genetic_parameters = SimpleNamespace()

genetic_parameters.initialPoolSize = 50
genetic_parameters.mergedNumber = 1
genetic_parameters.mutatedNumber = 1
genetic_parameters.randomNumber = 2


def rnd(n, b=0):
    return int(round(random.random() * (b - n) + n, 0))


def truncate_value(x, min_, max_):
    return max(min_, min(max_, x))


def get_data():

    my_x, my_y = [int(i) for i in input().split()]

    # fill humans_ list
    human_count = int(input())
    humans_ = []

    for i in range(human_count):
        human_id, human_x, human_y = [int(j) for j in input().split()]
        humans_.append(Human(human_id, human_x, human_y))

    # fill zombies list
    zombie_count = int(input())
    zombies_ = []

    for i in range(zombie_count):
        zombie_id, zombie_x, zombie_y, zombie_next_x, zombie_next_y = [int(j) for j in input().split()]
        zombies_.append(Zombie(zombie_id, zombie_x, zombie_y, zombie_next_x, zombie_next_y))

    return [my_x, my_y, humans_, zombies_]


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def multiply(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def truncate(self, max_value):
        i = max_value / self.magnitude()

        if i > 1:
            i = 1

        return self.multiply(i)

    def base_vector(self, point):
        return Vector(point.x - self.x, point.y - self.y)

    def move_to_target(self, point):

        direction_ = self.base_vector(point)

        if direction_.x != 0 or direction_.y != 0:
            direction_ = direction_.truncate(MY_MOVE_RANGE)

        return direction_


class Point(Vector):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def dist_square(self, point):
        x = self.x - point.x
        y = self.y - point.y
        return x ** 2 + y ** 2

    def dist(self, point):
        return math.sqrt(self.dist_square(point))


class Human(Point):
    def __init__(self, id_, x, y):
        super().__init__(x, y)
        self.id = id_
        self.alive = True


class Zombie(Point):
    def __init__(self, id_, x, y, next_x, next_y):
        super().__init__(x, y)
        self.id = id_
        self.next_x = next_x
        self.next_y = next_y
        self.alive = True


# update variables
data = get_data()

me = Point(data[0], data[1])
humans = data[2]
zombies = data[3]

humans_distance_square = [[human.dist_square(me), human] for human in humans]
closest_human = min(humans_distance_square, key=lambda x: x[0])

zombies_to_closest_human = [[zombie.dist_square(closest_human[1]), zombie] for zombie in zombies]
closest_zombie = min(zombies_to_closest_human, key=lambda x: x[0])

if closest_zombie[0] // ZOMBIE_MOVE_RANGE_SQUARE < me.dist_square(closest_human[1]) // MY_MOVE_RANGE_SQUARE:
    humans_distance_square = [human_array for human_array in humans_distance_square if human_array[1].id != closest_human[1].id]
    closest_human = min(humans_distance_square, key=lambda x: x[0])

print(f'closestHumanID: {closest_human[1].id}', file=sys.stderr, flush=True)

round_ = 0

while True:

    round_ += 1

    if round_ > 1:
        data = get_data()
        me = Point(data[0], data[1])

    direction = me.move_to_target(closest_human[1])

    print(f'x: {direction.x} y: {direction.y}', file=sys.stderr, flush=True)

    solution_x = truncate_value(me.x + direction.x, 0, 15999)
    solution_y = truncate_value(me.y + direction.y, 0, 8999)

    print(f'{round(solution_x)} {round(solution_y)}')

