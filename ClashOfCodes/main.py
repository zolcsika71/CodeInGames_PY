# IMPORT
from lib.classes.matrix_ import *
# END_IMPORT

n = int(input())
for k in range(n):
    line = input()

game = initialize(5, 5, 'A')
game.print_matrix()
