# Performance monitoring
import sys


def debug_time(msg, init, now):
    print(f"{msg} [{(now - init) * 1000:.3f}ms]", file=sys.stderr)
    sys.stderr.flush()
