import pygame
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

RESOLUTION = 800


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


class Graph:
    def __init__(self):
        self.destination = None
        self.start = None
        self.current = None
        self.nodes = {}
        self.path = []
        self.x_max = -math.inf
        self.y_max = -math.inf

    def run(self):
        self.get_input()
        print(f'x: {self.x_max} y: {self.y_max}')

    @staticmethod
    def coord_to_id(x_, y_):
        return str(x_) + ' ' + str(y_)

    @staticmethod
    def id_to_coord(cell_id):
        return [int(i) for i in cell_id.split()]

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

    def graph_dim_clouds(self, xi, yi, wi, hi):

        if xi + wi > self.x_max:
            self.x_max = xi + wi
        if yi + hi > self.y_max:
            self.y_max = yi + hi

    def graph_dim_coords(self, xs, ys, xd, yd):

        if xs > self.x_max:
            self.x_max = xs
        if xd > self.x_max:
            self.x_max = xd
        if ys > self.y_max:
            self.x_max = ys
        if yd > self.y_max:
            self.x_max = yd

    def extend_dim(self):
        self.x_max += 1
        self.y_max += 1


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def make_grid(row, col):
    grid = []
    gap = col // row
    for i in range(row):
        grid.append([])
        for j in range(row):
            spot = Spot(i, j, gap, row)
            grid[i].append(spot)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def main(win, row, col):
    grid = make_grid(row, col)

    run = True

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run = False

        draw(win, grid, row, col)

    pygame.quit()


graph = Graph()
graph.run()


def get_resolution(x, y):
    ratio_x = graph.x_max / graph.y_max
    ratio_y = graph.y_max / graph.x_max

    def adjust_res():
        row = int(RESOLUTION * ratio_y)
        col = int(RESOLUTION * ratio_x)

        print(f'{ratio_y} {ratio_x}')
        print(f'{row, col}')

    adjust_res()

    return 800, 800


WIDTH, HEIGHT = get_resolution(graph.x_max, graph.y_max)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Path Finding Algorithm")

main(WIN, graph.y_max, graph.x_max)
