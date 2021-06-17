import numpy as np
import math
from queue import PriorityQueue

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

RESOLUTION = 400


class Node:
    def __init__(self, row, col, rows=None, columns=None):
        self.neighbors = []
        self.row = row
        self.col = col
        self.rows = rows
        self.columns = columns
        self.closed = False
        self.open = False
        self.barrier = False
        self.start = False
        self.end = False
        self.path = False

    def get_pos(self):
        return self.row, self.col

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.rows - 1 and not grid[self.row + 1][self.col].is_barrier:  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier:  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.columns - 1 and not grid[self.row][self.col + 1].is_barrier:  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier:  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

        self.neighbors = np.array(self.neighbors)

    def __lt__(self, other):
        return False


class Graph:
    def __init__(self):
        self.grid = [[]]
        self.x_max = -math.inf
        self.y_max = -math.inf


class Main(Graph):
    def __init__(self):
        super().__init__()

    def get_input(self):

        # start
        xs, ys = [int(i) for i in input().split()]

        self.grid[xs][ys] = Node(xs, ys)

        # end
        end = [int(i) for i in input().split()]



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



