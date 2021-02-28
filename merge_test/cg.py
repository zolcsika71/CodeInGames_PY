# Normal library imports
# NOTE:  imports declared in imported functions need to be
#       manually added here for now...
import sys
import math
import time
# etc...


# Performance monitoring


def debug_time(msg, init, now):
    print(f"{msg} [{(now - init) * 1000:.3f}ms]", file=sys.stderr)
    sys.stderr.flush()


def second_func():
    print(f"Hello from Second: sqrt(10) = {math.sqrt(10)}")


def first_func():
    print("Hello from First", file=sys.stderr)
    second_func()


data = []


def run():
    init_t = time.time()
    first_func()
    debug_time(f"Time:", init_t, time.time())
    

run()
