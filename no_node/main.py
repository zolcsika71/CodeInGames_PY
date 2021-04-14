import numpy as np

columns = int(input())  # the number of cells on the X axis
rows = int(input())  # the number of cells on the Y axis

node_data = ''

for i in range(rows):
    line = input()  # width characters, each either 0 or .
    node_data += line

node_list = np.array(list(node_data))

node_list = node_list.reshape(rows, columns)


class Node:
    def __init__(self, rows_, columns_, row_, column_, matrix):
        self.rows = rows_
        self.columns = columns_
        self.row = row_
        self.column = column_
        self.matrix = matrix
        self.result = {
            'node_x': self.column,
            'node_y': self.row,
            'right_node_x': - 1,
            'bottom_node_y': - 1
        }
        self.result_array = []

        self.find_next_node()

    def find_next_node(self):

        if self.column + 1 != self.columns:
            for column_ in range(self.column + 1, self.columns):
                if node_list[self.row, column_] == '0':
                    self.result['right_node_x'] = column_
                    break

        if self.row + 1 != self.rows:
            for row_ in range(self.row + 1, self.rows):
                if node_list[row_, self.column] == '0':
                    self.result['bottom_node_y'] = row_
                    break

    def find_neighbors(self):

        self.result_array = [self.column, self.row]

        if self.result['right_node_x'] > - 1:
            if node_list[self.row, self.result['right_node_x']] == '.':
                self.result_array.extend([-1, -1])
            else:
                self.result_array.extend([self.result['right_node_x'], self.row])
        else:
            self.result_array.extend([-1, -1])

        if self.result['bottom_node_y'] > - 1:
            if node_list[self.result['bottom_node_y'], self.column] == '.':
                self.result_array.extend([-1, -1])
            else:
                self.result_array.extend([self.column, self.result['bottom_node_y']])
        else:
            self.result_array.extend([-1, -1])

        return self.result_array


nodes = []

for row in range(rows):
    for column in range(columns):
        if node_list[row, column] == '0':
            nodes.append(Node(rows, columns, row, column, node_list))

for node in nodes:
    print(' '.join(map(str, node.find_neighbors())))
