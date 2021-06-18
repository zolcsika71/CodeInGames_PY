import numpy as np
import math
from queue import PriorityQueue


class Node:
    def __init__(self, row, col, barrier, start, end):
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
        self.clouds = []
        self.start = []
        self.end = []
        self.graph = None
        self.start = None
        self.end = None
        self.columns = -math.inf
        self.rows = -math.inf

    def run(self):
        self.get_input()
        # self.make_grid()
        # self.get_neighbours()
        # self.print_graph()

    def get_input(self):

        # xs, ys
        self.start = [int(i) for i in input().split()]
        print(self.start)

        # xd, xs
        self.end = [int(i) for i in input().split()]
        print(self.end)

        n = int(input())

        for i in range(n):
            xi, yi, wi, hi = [int(j) for j in input().split()]

            self.clouds_extend_dim(xi, yi, wi, hi)
            self.clouds.append([xi, yi, wi, hi])

        self.coords_extend_dim(self.start, self.end)
        self.extend_dim()

        print(f'x: {self.columns} y: {self.columns}')

    def clouds_extend_dim(self, xi, yi, wi, hi):

        if xi + wi > self.columns:
            self.columns = xi + wi
        if yi + hi > self.rows:
            self.rows = yi + hi

    def coords_extend_dim(self, start, end):

        if start[0] > self.columns:
            self.columns = start[0]
        if start[1] > self.rows:
            self.rows = start[1]
        if end[0] > self.columns:
            self.columns = end[0]
        if end[1] > self.rows:
            self.rows = end[1]

    def extend_dim(self):
        self.columns += 1
        self.rows += 1

    def make_grid(self):

        self.graph = np.empty((self.rows, self.columns))

        for row in range(self.rows):
            for col in range(self.columns):
                # start node
                if row == self.start[1] and col == self.start[0]:
                    self.graph[row, col] = Node(row, col, False, True, False)
                # end node
                if row == self.end[1] and col == self.end[0]:
                    self.graph[row, col] = Node(row, col, False, False, True)
                # clouds
                for cloud in self.clouds:
                    pass

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
    print('Done')
