
# from ypstruct import structure
from copy import deepcopy
import random
import math


DEPTH = 3
MY_MOVE_RANGE = 1000
GENERATOR_RANGE = 3000


def rnd(n, b=0):
    return round(random.random() * (b - n) + n, 0)


def base_vector(point1, point2):
    return Vector(point2.number - point1.number, point2.y - point1.y)


def truncate_value(x, min_, max_):
    return max(min_, min(max_, x))


def fib(n):
    result = [0, 1]
    for n in range(2, n):
        a = result[n - 1]
        b = result[n - 2]
        result.append(a + b)

    return result[n]


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def multiply(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def truncate(self, max_value):
        n = max_value / self.magnitude()
        if n < 1:
            n = 1
        return self.multiply(n)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist_square(self, point):
        x = self.x - point.number
        y = self.y - point.y
        return x ** 2 + y ** 2

    def dist(self, point):
        return math.sqrt(self.dist_square(point))


class Sim(Point):
    def __init__(self, x, y, humans, zombies):
        super().__init__(x, y)
        self.cache = structure()
        self.humans = deepcopy(humans)
        self.zombies = deepcopy(zombies)
        self.zombie_killed = 0
        self.human_killed = 0

    def save(self):
        self.cache.number = self.x
        self.cache.y = self.y
        self.cache.humans = deepcopy(self.humans)
        self.cache.zombies = deepcopy(self.zombies)
        self.cache.zombie_killed = self.zombie_killed
        self.cache.human_killed = self.human_killed

    def load(self):
        self.x = self.cache.number
        self.y = self.cache.y
        self.humans = deepcopy(self.cache.humans)
        self.zombies = deepcopy(self.cache.zombies)
        self.zombie_killed = self.cache.zombie_killed
        self.human_killed = self.cache.human_killed

    def update(self, x, y, humans, zombies):
        self.x = x
        self.y = y
        self.humans = deepcopy(humans)
        self.zombies = deepcopy(zombies)


class Human(Point):
    def __init__(self, id_, x, y):
        super().__init__(x, y)
        self.id = id_
        self.alive = True

    def update(self, x, y):
        self.x = x
        self.y = y


class Zombie(Point):
    def __init__(self, id_, x, y, next_x, next_y):
        super().__init__(x, y)
        self.id = id_
        self.next_x = next_x
        self.next_y = next_y
        self.alive = True

    def update(self, x, y, next_x, next_y):
        self.x = x
        self.y = y
        self.next_x = next_x
        self.next_y = next_y


class Candidate:
    def __init__(self, id_):
        self.id = id_
        self.score = float('-inf')
        self.coords = []


class GeneticAlgorithm:
    def __init__(self):
        self.candidates = []
        self.evaluations = 0

    def generator(self, id_):

        candidate = Candidate(id_)
        r = rnd(1, DEPTH)

        for n in range(r):
            random_position = self.create_random_position()
            candidate.coords.append(random_position)

        return candidate

    def create_random_position(self):

        x = rnd(-GENERATOR_RANGE, GENERATOR_RANGE)
        y = rnd(-GENERATOR_RANGE, GENERATOR_RANGE)
        center_position = Point(0, 0)
        random_position = Point(x, y)
        direction = base_vector(center_position, random_position)

        return direction.truncate(MY_MOVE_RANGE)

    def merger(self, first_index, second_index):
        id_ = len(self.candidates)
        candidate_coords = self.candidates[first_index] + self.candidates[second_index]
        candidate_length = min(DEPTH, len(candidate_coords))
        random.shuffle(candidate_coords)
        candidate = Candidate(id_)
        candidate.coords = candidate_coords[:candidate_length - 1]

        return candidate

    def initialize(self, initial_pool_size):
        self.candidates = []
        self.add_candidates(initial_pool_size)

    def reset_scores(self):
        for candidate in problem.candidates:
            candidate.score = float('-inf')

    def add_candidates(self, number_of_candidates):
        for n in range(number_of_candidates):
            self.candidates.append(self.generator(n))

    def merge(self, merged_number):
        first_index = None
        second_index = None
        for n in range(merged_number):
            candidates_length = len(self.candidates)
            first_index = rnd(candidates_length - 1)
            second_index = (first_index + rnd(candidates_length - 1)) % candidates_length

        self.candidates.append(self.merger(first_index, second_index))










problem = GeneticAlgorithm()
# me = Sim()


# read all data

# my position
my_x, my_y = [int(n) for n in input().split()]


# fill humans list
human_count = int(input())
humans = []

for n in range(human_count):
    human_id, human_x, human_y = [int(j) for j in input().split()]
    humans.append(Human(human_id, human_x, human_y))


zombie_count = int(input())
zombies = []

for n in range(zombie_count):
    zombie_id, zombie_x, zombie_y, zombie_next_x, zombie_next_y = [int(j) for j in input().split()]
    zombies.append(Zombie(zombie_id, zombie_x, zombie_y, zombie_next_x, zombie_next_y))





class CandidateOperations:
    def generator(self, id_):

        candidate = Candidate(id_)
        r = rnd(1, DEPTH)

        for n in range(r):
            random_position = self.create_random_position()
            candidate.coords.append(random_position)

        return candidate

    def create_random_position(self):

        x = rnd(-GENERATOR_RANGE, GENERATOR_RANGE)
        y = rnd(-GENERATOR_RANGE, GENERATOR_RANGE)
        center_position = Point(0, 0)
        random_position = Point(x, y)
        direction = base_vector(center_position, random_position)

        return direction.truncate(MY_MOVE_RANGE)

    def merger(self, first_index, second_index):
        id_ = len(problem.candidates)
        candidate_coords = problem.candidates[first_index] + problem.candidates[second_index]
        candidate_length = min(DEPTH, len(candidate_coords))
        random.shuffle(candidate_coords)
        candidate = Candidate(id_)
        candidate.coords = candidate_coords[:candidate_length - 1]

        return candidate

    def mutator(self):
        id_ = len(problem.candidates)
        random_position = self.create_random_position()
        candidate_index = rnd(0, len(problem.candidates) - 1)
        candidate_step = rnd(0, len(problem.candidates[candidate_index].coords) - 1)
        candidate_coords = deepcopy(problem.candidates[candidate_index].coords)
        candidate_coords[candidate_step] = random_position
        candidate = Candidate(id_)
        candidate.coords = candidate_coords

        return candidate


















































