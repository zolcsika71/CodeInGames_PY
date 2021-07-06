import sys
import math

moving_player_, white_king_, white_rook_, black_king_ = input().split()


def position(col, row):
    return str(col) + str(row)


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


class Cell:
    def __init__(self, char):
        self.visited = False
        self.distance = math.inf
        self.char = char
        self.possible_positions = None


class Board:
    def __init__(self, moving_player, white_king, white_rook, black_king):
        self.moving_player = moving_player
        self.white_king = position_to_numbers(white_king)
        self.white_rook = position_to_numbers(white_rook)
        self.black_king = position_to_numbers(black_king)
        self.column = 8
        self.row = 8
        self.board = {}
        self.init_board()
        self.print_positions()

    def init_board(self):
        print(f'moving_player: {self.moving_player}', file=sys.stderr, flush=True)
        print(f'white_king: {self.white_king}', file=sys.stderr, flush=True)
        print(f'white_rook: {self.white_rook}', file=sys.stderr, flush=True)
        print(f'black_king: {self.black_king}', file=sys.stderr, flush=True)
        char = None
        wk_positions = None
        bk_positions = None
        wr_positions = None
        for row in range(1, self.row + 1):
            for column in range(1, self.column + 1):
                pos = position(column, row)
                if pos == self.white_king:
                    char = 'WK'
                    wk_positions = set([pos for pos in self.legal_moves_from(column, row, char)])
                elif pos == self.black_king:
                    char = 'BK'
                    bk_positions = set([pos for pos in self.legal_moves_from(column, row, char)])
                elif pos == self.white_rook:
                    char = 'WR'
                    wr_positions = set([pos for pos in self.legal_moves_from(column, row, char)])

                self.board[pos] = Cell(char)

        self.board[self.white_king].possible_positions = wk_positions.difference(bk_positions)
        self.board[self.black_king].possible_positions = bk_positions.difference(wk_positions)
        self.board[self.white_rook].possible_positions = wr_positions

    def legal_moves_from(self, col, row, char):
        king_offset = (
            (-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)
        )
        if char is None:
            return
        elif char == 'WK' or char == 'BK':
            for col_offset, row_offset in king_offset:
                move_col, move_row = col + col_offset, row + row_offset
                if 1 <= move_col <= self.column and 1 <= move_row <= self.row:
                    yield position(move_col, move_row)

        elif char == 'WR':
            for move_row in range(1, self.row):
                if move_row != row:
                    yield position(col, move_row)
            for move_col in range(1, self.column):
                if move_col != col:
                    yield position(move_col, row)

    def print_positions(self):
        print(f'WK_moves: {self.board[self.white_king].possible_positions}', file=sys.stderr, flush=True)
        print(f'BK_moves: {self.board[self.black_king].possible_positions}', file=sys.stderr, flush=True)
        print(f'WR_moves: {self.board[self.white_rook].possible_positions}', file=sys.stderr, flush=True)
        # for move in self.board[self.white_rook].possible_positions:
        #     print(f'{self.position_to_letters(move)}', file=sys.stderr, flush=True)


chess = Board(moving_player_, white_king_, white_rook_, black_king_)

print('e3d3')
