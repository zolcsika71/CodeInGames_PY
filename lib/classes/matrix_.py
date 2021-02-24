def initialize(rows, columns, value=0):
    return Matrix(rows, columns, value)


class Matrix(object):
    def __init__(self, rows, columns, value):
        self.rows = rows
        self.columns = columns
        self.line = 'ABCDEFGHI'  # length = (rows - 2) * (columns - 2)
        self.matrix = []
        for i in range(rows):
            self.matrix.append([value for j in range(columns)])

        # self.update_table()

    def __getitem__(self, index):
        return self.matrix[index]

    def update_table(self):

        print(f'line: {self.line}')
        x = 1
        y = 1

        for char in self.line:
            self[x][y] = char
            if y == self.columns - 2:
                y = 1
                x += 1
            else:
                y += 1

    def print_matrix(self):
        self.update_table()
        for row in range(self.rows):
            for column in range(self.columns):
                print(self[row][column], end='')
            print('\r')
