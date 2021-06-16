import sys
import math
import numpy as np


# Write an answer using print
# To debug: print(f'Debug messages...', file=sys.stderr, flush=True)


class Graph:
    def __init__(self):
        self.destination = None
        self.start = None
        self.current = None
        self.nodes = {}
        self.path = []
        self.x_min = math.inf
        self.x_max = -math.inf
        self.y_min = math.inf
        self.y_max = -math.inf

    @staticmethod
    def coord_to_id(x_, y_):
        return str(x_) + ' ' + str(y_)

    @staticmethod
    def id_to_coord(cell_id):
        return [int(i) for i in cell_id.split()]

    def run(self):
        self.get_input()
        # self.print_graph()
        distance = self.solve()
        print(distance)

    def graph_dim_clouds(self, xi, yi, wi, hi):

        if xi < self.x_min:
            self.x_min = xi
        if xi + wi > self.x_max:
            self.x_max = xi + wi

        if yi < self.y_min:
            self.y_min = yi
        if yi + hi > self.y_max:
            self.y_max = yi + hi

    def graph_dim_coords(self, xs, ys, xd, yd):

        if xs < self.x_min:
            self.x_min = xs
        if xs > self.x_max:
            self.x_max = xs

        if xd < self.x_min:
            self.x_min = xd
        if xd > self.x_max:
            self.x_max = xd

        if ys < self.y_min:
            self.y_min = ys
        if ys > self.y_max:
            self.x_max = ys

        if yd < self.y_min:
            self.y_min = yd
        if yd > self.y_max:
            self.x_max = yd

    def extend_dim(self):
        self.x_min -= 1
        self.x_max += 1
        self.y_min -= 1
        self.y_max += 1

    def get_neighbours(self, x, y):
        neighbours = []

        def add_neighbour(direction):
            if direction not in self.nodes.keys() or (not self.nodes[direction]['cloudy'] and not self.nodes[direction]['visited']):
                neighbours.append(direction)

        if not x <= self.x_min:
            left = self.coord_to_id(x - 1, y)
            add_neighbour(left)
        if not x >= self.x_max:
            right = self.coord_to_id(x + 1, y)
            add_neighbour(right)
        if not y <= self.y_min:
            top = self.coord_to_id(x, y - 1)
            add_neighbour(top)
        if not y >= self.y_max:
            down = self.coord_to_id(x, y + 1)
            add_neighbour(down)

        return neighbours

    def get_input(self):
        xs, ys = [int(i) for i in input().split()]
        cell_id = self.coord_to_id(xs, ys)
        self.add_node(cell_id, 0, False)

        xd, yd = [int(i) for i in input().split()]
        cell_id = self.coord_to_id(xd, yd)
        self.add_node(cell_id, math.inf, False)

        self.current = self.start = self.coord_to_id(xs, ys)
        self.destination = self.coord_to_id(xd, yd)

        n = int(input())

        for i in range(n):
            xi, yi, wi, hi = [int(j) for j in input().split()]

            self.graph_dim_clouds(xi, yi, wi, hi)

            for x in range(xi, xi + wi):
                for y in range(yi, yi + hi):
                    cell_id = self.coord_to_id(x, y)
                    self.add_node(cell_id, math.inf, True)

        # print(self.x_min, self.y_min, self.x_max, self.y_max)

        self.graph_dim_coords(xs, ys, xd, yd)
        self.extend_dim()

        # print(self.x_min, self.y_min, self.x_max, self.y_max)

    def add_node(self, cell_id, distance, cloudy, visited=False):
        self.nodes[cell_id] = {
            'distance': distance,
            'cloudy': cloudy,
            'visited': visited
        }

    def update_node(self, cell_id, distance):
        if self.nodes[cell_id]['distance'] > distance:
            self.nodes[cell_id]['distance'] = distance

    def solve(self):
        x, y = self.id_to_coord(self.current)

        # print(self.x_min, self.y_min, self.x_max,  self.y_max)

        neighbours = self.get_neighbours(x, y)

        for neigh in neighbours:
            if neigh not in self.nodes.keys():
                distance = self.nodes[self.current]['distance'] + 1
                self.add_node(neigh, distance, False)
            else:
                distance = self.nodes[self.current]['distance'] + 1
                self.update_node(neigh, distance)

        self.nodes[self.current]['visited'] = True

        # print(f'{self.current}')
        print(f'neighbours: {neighbours}')

        if len(neighbours) > 0:
            self.current = self.next_node(neighbours)
            print(f'next node {self.current} {self.nodes[self.current]}')
            if self.current != self.destination:
                self.solve()

        return self.nodes[self.current]['distance']

    def next_node(self, neighbors):
        min_dist = min(self.nodes[neigh]['distance'] for neigh in neighbors)
        return [neigh for neigh in neighbors if self.nodes[neigh]['distance'] == min_dist][0]

    def print_graph(self):
        print(self.y_max, self.x_max)
        table = np.full((self.y_max, self.x_max), ".", dtype=str)
        for node in self.nodes.keys():
            x, y = self.id_to_coord(node)
            if node == self.start:
                char = 'S'
            elif node == self.destination:
                char = 'D'
            else:
                char = '#'

            table[y, x] = char

        for el in table:
            print('  '.join(el.astype(str)))


graph = Graph()
graph.run()
