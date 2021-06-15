class Board:
    def __init__(self, cells):
        self.cells = cells


class Game(Board):
    def __init__(self, cells, day, counter):
        super().__init__(cells)
        self.day = 0
        self.counter = 0


class Display(Game):
    def __init__(self):
        super().__init__()

    def print_game(self):
        print(f'{self.day}')
        print(f'{self.cells}')


board = Board()
game = Game()


board.cells.append(10)
game.day = 1
game.counter = 2

display = Display()

display.print_game()







