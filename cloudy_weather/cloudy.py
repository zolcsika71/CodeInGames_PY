import numpy as np
import math
from queue import PriorityQueue


class Node:
    def __init__(self, col, row, barrier, start, end):
        self.neighbors = []
        self.row = row
        self.col = col
        self.closed = False
        self.open = False
        self.barrier = barrier
        self.start = start
        self.end = end
        self.path = False

    def get_pos(self):
        return self.row, self.col

    def update_neighbors(self, grid, rows, columns):
        self.neighbors = []
        # DOWN
        if self.row < rows - 1 and not grid[self.row + 1][self.col].barrier:
            self.neighbors.append(grid[self.row + 1][self.col])

        # UP
        if self.row > 0 and not grid[self.row - 1][self.col].barrier:
            self.neighbors.append(grid[self.row - 1][self.col])

        # RIGHT
        if self.col < columns - 1 and not grid[self.row][self.col + 1].barrier:
            self.neighbors.append(grid[self.row][self.col + 1])

        # LEFT
        if self.col > 0 and not grid[self.row][self.col - 1].barrier:
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


class Main:
    def __init__(self):
        self.nodes = {}
        self.graph = []
        self.start = None
        self.end = None
        self.columns = -math.inf
        self.rows = -math.inf

    @staticmethod
    def coord_to_id(x_, y_):
        return str(x_) + ' ' + str(y_)

    @staticmethod
    def id_to_coord(cell_id):
        return [int(i) for i in cell_id.split()]

    def run(self):
        self.get_input()
        self.make_grid()
        self.get_neighbours()
        # self.print_graph()

    def get_input(self):
        xs, ys = [int(i) for i in input().split()]
        self.add_node(xs, ys, False, True, False)

        xd, yd = [int(i) for i in input().split()]
        self.add_node(xd, yd, False, False, True)

        n = int(input())

        for i in range(n):
            xi, yi, wi, hi = [int(j) for j in input().split()]

            self.clouds_extend_dim(xi, yi, wi, hi)

            for x in range(xi, xi + wi):
                for y in range(yi, yi + hi):
                    self.add_node(x, y, True, False, False)

        self.coords_extend_dim(xs, ys, xd, yd)
        self.extend_dim()

    def add_node(self, col, row, barrier, start, end):
        self.nodes[self.coord_to_id(col, row)] = Node(col, row, barrier, start, end)

    def clouds_extend_dim(self, xi, yi, wi, hi):

        if xi + wi > self.columns:
            self.columns = xi + wi
        if yi + hi > self.rows:
            self.rows = yi + hi

    def coords_extend_dim(self, xs, ys, xd, yd):

        if xs > self.columns:
            self.columns = xs
        if xd > self.columns:
            self.columns = xd
        if ys > self.rows:
            self.rows = ys
        if yd > self.rows:
            self.rows = yd

    def extend_dim(self):
        self.columns += 1
        self.rows += 1

    def make_grid(self):
        for row in range(self.rows):
            self.graph.append([])
            for col in range(self.columns):
                try:
                    node = self.nodes[self.coord_to_id(col, row)]
                    if node.start:
                        self.start = node
                    if node.end:
                        self.end = node

                    self.graph[row].append(node)

                except KeyError:
                    node = Node(col, row, False, False, False)
                    self.graph[row].append(node)

    def get_neighbours(self):
        for row in self.graph:
            for col in row:
                col.update_neighbors(self.graph, self.rows, self.columns)

    def print_graph(self):
        print(self.columns, self.rows)
        table = np.full((self.rows, self.columns), ".", dtype=str)
        for row in self.graph:
            for col in row:
                if col == self.start:
                    char = 'S'
                elif col == self.end:
                    char = 'D'
                elif col.barrier:
                    char = '#'
                else:
                    char = '.'

                table[col.row, col.col] = char

        for el in table:
            print(''.join(el.astype(str)))


if __name__ == '__main__':
    main = Main()
    main.run()
