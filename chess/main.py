import sys
import math

moving_player, white_king_, white_rook_, black_king_ = input().split()

print(f'moving_player: {moving_player}', file=sys.stderr, flush=True)
print(f'white_king: {white_king_}', file=sys.stderr, flush=True)
print(f'white_rook: {white_rook_}', file=sys.stderr, flush=True)
print(f'black_king: {black_king_}', file=sys.stderr, flush=True)


def position(col, row):
    return str(col) + str(row)


class Cell:
    def __init__(self, col, row, char=None):
        self.col = col
        self.row = row
        self.visited = False
        self.char = char
        self.possible_positions = None
        self.get_positions()

    def get_positions(self):
        king_move = (
            (-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)
        )
        if self.char is None:
            return
        elif self.char == 'WK' or self.char == 'BK':
            self.possible_positions = []
            for pos in king_move:
                col = self.col + pos[0]
                row = self.row + pos[1]
                if 1 <= col <= 8 or 1 <= row <= 8:
                    self.possible_positions.append(position(col, row))

        elif self.char == 'WR':
            pass


class Board:
    def __init__(self):
        self.column = 8
        self.row = 8
        self.board = {}

    @staticmethod
    def position_to_letters(pos):
        column = pos[0]
        row = pos[1]
        columns = {
            '1': 'a',
            '2': 'b',
            '3': 'c',
            '4': 'd',
            '5': 'e',
            '6': 'f',
            '7': 'g',
            '8': 'h',
        }

        return columns[column] + str(row)

    @staticmethod
    def position_to_numbers(pos):
        column = pos[0]
        row = pos[1]
        columns = {
            'a': '1',
            'b': '2',
            'c': '3',
            'd': '4',
            'e': '5',
            'f': '6',
            'g': '7',
            'h': '8',
        }

        return columns[column] + str(row)

    def init_board(self):
        white_king = self.position_to_numbers(white_king_)
        white_rook = self.position_to_numbers(white_rook_)
        black_king = self.position_to_numbers(black_king_)
        char = None
        for row in range(1, self.row):
            for column in range(1, self.column):
                pos = position(column, row)
                if pos == white_king:
                    char = 'WK'
                elif pos == white_rook:
                    char = 'WR'
                elif pos == black_king:
                    char = 'BK'
                self.board[pos] = Cell(column, row, char)


print('f8g8 b1e1')
