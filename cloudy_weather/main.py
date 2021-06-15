import sys
import math


# Write an answer using print
# To debug: print(f'Debug messages...', file=sys.stderr, flush=True)


class Graph:
    def __init__(self):
        self.destination = None
        self.current = None
        self.nodes = {}
        self.path = []

    @staticmethod
    def coord_to_id(x_, y_):
        return str(x_) + ' ' + str(y_)

    @staticmethod
    def id_to_coord(cell_id):
        return [int(i) for i in cell_id.split()]

    def run(self):
        self.get_input()
        self.solve()

    def get_input(self):
        xs, ys = [int(i) for i in input().split()]

        cell_id = self.coord_to_id(xs, ys)

        self.add_node(cell_id, 0, False)

        xd, yd = [int(i) for i in input().split()]

        cell_id = self.coord_to_id(xd, yd)

        self.add_node(cell_id, math.inf, False)

        n = int(input())

        for i in range(n):
            xi, yi, wi, hi = [int(j) for j in input().split()]
            for x in range(xi, xi + wi):
                for y in range(yi, yi + hi):
                    cell_id = self.coord_to_id(x, y)
                    self.add_node(cell_id, math.inf, True)

        self.current = self.coord_to_id(xs, ys)
        self.destination = self.coord_to_id(xd, yd)

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
        self.update_graph()

    def update_graph(self):
        x, y = self.id_to_coord(self.current)

        left = self.coord_to_id(x - 1, y)
        right = self.coord_to_id(x + 1, y)
        top = self.coord_to_id(x, y - 1)
        down = self.coord_to_id(x, y + 1)

        neighbors = [left, right, top, down]

        for neigh in neighbors:
            if neigh not in self.nodes.keys():
                distance = self.nodes[self.current]['distance'] + 1
                self.add_node(neigh, distance, False)
            elif not self.nodes[neigh]['cloudy'] or not self.nodes[neigh]['visited']:
                distance = self.nodes[self.current]['distance'] + 1
                self.update_node(neigh, distance)

        self.nodes[self.current]['visited'] = True

        print(f'current: {self.current} {self.nodes[self.current]}')

        next_node = self.next_node(neighbors)

        print(f'next node {next_node}')

    def next_node(self, neighbors):
        return min(neigh['distance'] for neigh in self.nodes[neighbors] if not neigh['visited'])


graph = Graph()
graph.run()

print(f'start: {graph.current} destination: {graph.destination}')
