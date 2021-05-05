import sys
import math

# Detect which particle just passed through the cloud chamber,
# if unknown, you may win the Nobel prize of physics!

w = int(input())  # width of ASCII-art picture (one meter per column)
h = int(input())  # height of ASCII-art picture (one meter per line)
b = float(input())  # strengh of magnetic field (tesla)
v = float(input())  # speed of the particle (speed-of-light unit)
for i in range(h):
    line = input()  # lines of ASCII-art picture

# Write an answer using print
# To debug: print("Debug messages...", file=sys.stderr, flush=True)


# "<symbol> <radius>" if charged particle
# "<symbol> inf" if neutral particle
# "I just won the Nobel prize in physics !" if unknown particle
print("symbol radius")
