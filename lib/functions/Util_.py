# Utils
import sys


def debug_time(msg, init, now):
    print(f"{msg} [{(now - init) * 1000:.3f}ms]", file=sys.stderr)
    sys.stderr.flush()


def fib(n_, a_, b_):
    result_ = [a_, b_]
    for n_ in range(2, n_ + 1):
        a_ = result_[n_ - 1]
        b_ = result_[n_ - 2]
        result_.append(a_ + b_)

    return result_
