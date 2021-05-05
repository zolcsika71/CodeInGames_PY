import sys
import numpy as np
import string

THRESHOLD = 1
NON_TERMINAL_CHARS = list(string.ascii_uppercase[::-1])

test_one = False

if test_one:
    n = 1
    m = 11
    lines = np.array(['a', 'a', 'a', 'b', 'd', 'a', 'a', 'a', 'b', 'a', 'c'])
else:
    n = 2
    m = 10
    lines = np.array(
        ['Z', 'a', 'b', 'd', 'Z', 'a', 'b', 'a', 'c']
    )

print(f'orig line: {lines}', file=sys.stderr, flush=True)


def get_byte_pairs(lines_):
    if m % 2 != 0:
        lines_ = np.append(lines_, [' '])

    byte_pairs_dict = {}
    byte_pairs_arr = np.array([])

    print(f'line: {lines_}', file=sys.stderr, flush=True)

    for idx in range(len(lines_) - 1):
        byte_pairs_dict[idx] = np.array([lines_[idx] + lines_[idx + 1]])

    idx = 0
    max_idx = len(byte_pairs_dict) - 2

    print(f'max_idx: {max_idx}', file=sys.stderr, flush=True)

    while idx < max_idx:
        print(f'idx: {idx}', file=sys.stderr, flush=True)
        if byte_pairs_dict[idx] == byte_pairs_dict[idx + 1]:
            print(f'overlap: {idx} {byte_pairs_dict[idx]}', file=sys.stderr, flush=True)
            byte_pairs_arr = np.concatenate((byte_pairs_arr, byte_pairs_dict[idx]))
            idx += 2
        else:
            print(f'unique: {idx} {byte_pairs_dict[idx]}', file=sys.stderr, flush=True)
            byte_pairs_arr = np.concatenate((byte_pairs_arr, byte_pairs_dict[idx]))
            idx += 1

    return byte_pairs_arr


byte_pairs = get_byte_pairs(lines)

print(f'byte_pairs: {byte_pairs}', file=sys.stderr, flush=True)

# reshape odd number of element to 2d
# byte_pairs = np.full((rows, columns), np.nan, dtype='object')
# byte_pairs.ravel()[:len(lines)] = lines
