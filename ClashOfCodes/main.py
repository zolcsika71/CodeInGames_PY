import sys
import math

# IMPORT
from lib.functions.Util_ import *
# END_IMPORT

t = int(input())
a = int(input())
b = int(input())

results = fib(t, a, b)

for result in results:
    print(result)
