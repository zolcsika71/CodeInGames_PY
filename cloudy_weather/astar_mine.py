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

RESOLUTION = 400


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


class Spot:
    def __init__(self, row, col, gap_rows, gap_columns, total_rows, total_columns):
        self.row = row
        self.col = col
        self.x = col * gap_columns
        self.y = row * gap_rows
        self.color = WHITE
        self.neighbors = []
        self.gap_rows = gap_rows
        self.gap_columns = gap_columns
        self.total_rows = total_rows
        self.total_columns = total_columns

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
        pygame.draw.rect(win, self.color, (self.x, self.y, self.gap_columns, self.gap_rows))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_columns - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def make_grid(row_res, col_res, rows, columns):
    grid = []
    gap_rows = row_res / rows
    gap_columns = col_res / columns
    start = None
    end = None

    for row in range(rows):
        grid.append([])
        for col in range(columns):
            spot = Spot(row, col, gap_rows, gap_columns, rows, columns)
            grid[row].append(spot)
            node_key = graph.coord_to_id(col, row)
            if graph.destination == node_key:
                grid[row][col].make_end()
                end = grid[row][col]
            if graph.start == node_key:
                grid[row][col].make_start()
                start = grid[row][col]
            try:
                if graph.nodes[node_key]['cloudy']:
                    grid[row][col].make_barrier()
            except KeyError:
                pass

    return grid, gap_rows, gap_columns, start, end


def draw_grid(win, rows, columns, gap_rows, gap_columns):
    for row in range(rows):
        pygame.draw.line(win, GREY, (0, row * gap_rows), (COL, row * gap_rows))
        for col in range(columns):
            pygame.draw.line(win, GREY, (col * gap_columns, 0), (col * gap_columns, ROW))


def draw(win, grid, rows, columns, gap_rows, gap_columns):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, columns, gap_rows, gap_columns)
    pygame.display.update()


def reconstruct_path(came_from, current, draw_):
    counter = 0
    while current in came_from:
        current = came_from[current]
        current.make_path()
        counter += 1

    return counter


def algorithm(draw_, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            counter = reconstruct_path(came_from, end, draw_)
            end.make_end()
            return counter

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        if current != start:
            current.make_closed()

    return False


def main(win, row_res, col_res, rows, columns):
    grid, gap_rows, gap_columns, start, end = make_grid(row_res, col_res, rows, columns)
    shortest = math.inf
    run = True

    while run:

        draw(win, grid, rows, columns, gap_rows, gap_columns)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    shortest = algorithm(lambda: draw(win, grid, rows, columns, gap_rows, gap_columns),
                                         grid, start, end)

    print(shortest)

    pygame.quit()


graph = Graph()
graph.run()


def get_resolution(x, y):
    ratio_x = x / y
    ratio_y = y / x
    row_ = int(RESOLUTION * ratio_y)
    col_ = int(RESOLUTION * ratio_x)
    mod_x = col_ % x
    mod_y = row_ % y

    if mod_x != 0:
        col_ += x - mod_x

    if mod_y != 0:
        row_ += y - mod_y

    return row_, col_


ROW, COL = get_resolution(graph.x_max, graph.y_max)

print(f'x: {graph.x_max} y: {graph.y_max}')
print(f'col: {COL} row: {ROW}')

WIN = pygame.display.set_mode((COL, ROW))
pygame.display.set_caption("A* Path Finding Algorithm")

main(WIN, ROW, COL, graph.y_max, graph.x_max)
