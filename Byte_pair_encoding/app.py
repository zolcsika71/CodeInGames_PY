import sys
import numpy as np
import string
import math

THRESHOLD = 1
NON_TERMINAL_CHARS = list(string.ascii_uppercase[::-1])

lines = np.array([])

n, m = [int(i) for i in input().split()]

for i in range(n):
    line = np.array(list(input()))
    lines = np.concatenate((lines, line))


def get_byte_pairs(lines_):
    byte_pairs_dict = {}
    byte_pairs_arr = np.array([])

    for idx in range(len(lines_)):
        try:
            byte_pairs_dict[idx] = np.array([lines_[idx] + lines_[idx + 1]])
        except IndexError:
            byte_pairs_dict[idx] = np.array([lines_[idx]])

    idx = 0
    max_idx = len(byte_pairs_dict) - 1

    while idx < max_idx:

        if byte_pairs_dict[idx] == byte_pairs_dict[idx + 1]:

            byte_pairs_arr = np.concatenate((byte_pairs_arr, byte_pairs_dict[idx]))
            idx += 2
        else:
            byte_pairs_arr = np.concatenate((byte_pairs_arr, byte_pairs_dict[idx]))
            idx += 1

    return byte_pairs_arr


def get_most_common_pair(byte_pairs_):
    unique, idx, counts = np.unique(byte_pairs_, return_counts=True, return_index=True)

    counts_filter = tuple([counts > THRESHOLD])
    byte_pairs_filtered = byte_pairs_[idx[counts_filter]]
    counts = counts[counts_filter]

    if len(counts) > 0:

        count_max = np.amax(counts)
        count_max_idx = np.where(counts == count_max)[0]

        index = math.inf

        for i in count_max_idx:
            get_index = np.where(byte_pairs_ == byte_pairs_filtered[i])[0][0]
            if get_index < index:
                index = get_index

        byte_pair_ = str(byte_pairs_[index])

        return byte_pair_

    else:
        return None


def replace_byte_pair(lines_, byte_pair_, NTC_idx_):
    idx = 0
    max_idx = len(lines_) - 1

    while idx < max_idx:

        if lines_[idx] == byte_pair_[0] and lines_[idx + 1] == byte_pair_[1]:

            lines_[idx] = NON_TERMINAL_CHARS[NTC_idx_]
            lines_ = np.delete(lines_, idx + 1)
            max_idx = len(lines_) - 1

            idx += 1
        else:
            idx += 1

    return lines_


NTC_idx = 0
prod_rules = {}

while True:

    byte_pairs = get_byte_pairs(lines)

    byte_pair = get_most_common_pair(byte_pairs)

    if byte_pair:

        prod_rules[NON_TERMINAL_CHARS[NTC_idx]] = byte_pair
        lines = replace_byte_pair(lines, byte_pair, NTC_idx)

        NTC_idx += 1
    else:
        break

print(''.join(lines).strip())
for rule in prod_rules:
    print(f'{rule} = {prod_rules[rule]}')
