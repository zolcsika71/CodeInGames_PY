import sys
import math
import numpy as np

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

h = int(input())
w = int(input())
matrix = np.array([])

x, y = [int(i) for i in input().split()]

for i in range(h):
    row = np.array(list(input()))
    matrix = np.concatenate((row, matrix))

matrix = matrix.reshape(h, w)

print(matrix[x - 1][y])
