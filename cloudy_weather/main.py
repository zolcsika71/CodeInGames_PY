import sys
import math


# Write an answer using print
# To debug: print(f'Debug messages...', file=sys.stderr, flush=True)


class Graph:
    def __init__(self):
        self.start = None
        self.destination = None
        self.current = None
        self.nodes = {}
        self.path = []

    @staticmethod
    def coord_to_id(x_, y_):
        return str(x_) + ' ' + str(y_)

    @staticmethod
    def id_to_coord(object_id):
        return [int(i) for i in object_id.split()]

    def run(self):
        self.get_input()

    def get_input(self):
        xs, ys = [int(i) for i in input().split()]

        self.add_node(xs, ys, 0, False)

        xd, yd = [int(i) for i in input().split()]

        self.add_node(xd, yd, math.inf, False)

        n = int(input())

        for i in range(n):
            xi, yi, wi, hi = [int(j) for j in input().split()]
            for x in range(xi, xi + wi):
                for y in range(yi, yi + hi):
                    self.add_node(x, y, math.inf, True)

        self.start = self.current = self.coord_to_id(xs, ys)
        self.destination = self.coord_to_id(xd, yd)

    def add_node(self, x_, y_, distance, cloudy, visited=False):
        object_id = self.coord_to_id(x_, y_)
        self.nodes[object_id] = {
            'distance': distance,
            'cloudy': cloudy,
            'visited': visited
        }

    def get_neighbours(self):
        x, y = self.id_to_coord(self.current)

        left = self.coord_to_id(x - 1, y)
        right = self.coord_to_id(x + 1, y)
        top = self.coord_to_id(x, y - 1)
        down = self.coord_to_id(x, y + 1)

        if self.nodes[left] is None:
            self.add_node(x - 1, y, 1, False)
        if self.nodes[right] is None:
            self.add_node(x + 1, y, 1, False)
        if self.nodes[top] is None:
            self.add_node(x, y - 1, 1, False)
        if self.nodes[down] is None:
            self.add_node(x, y + 1, False)


graph = Graph()
