import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

n = int(input())

# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr, flush=True)

if (n // 4) % 2 < n:
    print(f'{(n // 4)}')
else:
    print(f'{(n // 4) + 1}')
