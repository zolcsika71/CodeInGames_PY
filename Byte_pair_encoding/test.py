import sys
import numpy as np
import string
import math

THRESHOLD = 1
NON_TERMINAL_CHARS = list(string.ascii_uppercase[::-1])

test = 3

if test == 1:
    n = 1
    m = 11
    lines = np.array(
        list('aaabdaaabac')
    )
elif test == 2:
    n = 2
    m = 10
    lines = np.array(
        list('aedcaafffbddcaaacdcd')
    )
elif test == 3:
    n = 4
    m = 10
    lines = np.array(
        list('aaaaaaaaaaaaaaabbbbbbbbbbbbbbbcccccccccc')
    )


def get_byte_pairs(lines_):
    # if len(lines_) % 2 != 0:
    #     lines_ = np.append(lines_, [' '])

    byte_pairs_dict = {}
    byte_pairs_arr = np.array([])

    # print(f'line: {lines_}', file=sys.stderr, flush=True)

    for idx in range(len(lines_)):
        try:
            byte_pairs_dict[idx] = np.array([lines_[idx] + lines_[idx + 1]])
        except IndexError:
            byte_pairs_dict[idx] = np.array([lines_[idx]])

    idx = 0
    max_idx = len(byte_pairs_dict) - 1

    # print(f'max_idx: {max_idx}', file=sys.stderr, flush=True)
    # print(f'dict: {byte_pairs_dict}', file=sys.stderr, flush=True)

    while idx < max_idx:
        # print(f'idx: {idx}', file=sys.stderr, flush=True)
        if byte_pairs_dict[idx] == byte_pairs_dict[idx + 1]:
            # print(f'overlap: {idx} {byte_pairs_dict[idx]}', file=sys.stderr, flush=True)
            byte_pairs_arr = np.concatenate((byte_pairs_arr, byte_pairs_dict[idx]))
            idx += 2
        else:
            # print(f'unique: {idx} {byte_pairs_dict[idx]}', file=sys.stderr, flush=True)
            byte_pairs_arr = np.concatenate((byte_pairs_arr, byte_pairs_dict[idx]))
            idx += 1

    return byte_pairs_arr


def get_most_common_pair(byte_pairs_):
    unique, idx, counts = np.unique(byte_pairs_, return_counts=True, return_index=True)

    counts_filter = tuple([counts > THRESHOLD])
    byte_pairs_filtered = byte_pairs_[idx[counts_filter]]
    counts = counts[counts_filter]

    print(f'unique: {unique}', file=sys.stderr, flush=True)
    print(f'counts_filter: {counts_filter}', file=sys.stderr, flush=True)
    print(f'counts: {counts}', file=sys.stderr, flush=True)
    print(f'byte_pairs_filtered: {byte_pairs_filtered}', file=sys.stderr, flush=True)

    if len(counts) > 0:

        count_max = np.amax(counts)
        count_max_idx = np.where(counts == count_max)[0]
        print(f'count_max_idx: {count_max_idx}', file=sys.stderr, flush=True)

        index = math.inf

        for i in count_max_idx:
            get_index = np.where(byte_pairs_ == byte_pairs_filtered[i])[0][0]
            if get_index < index:
                index = get_index

        print(f'index: {index}', file=sys.stderr, flush=True)

        # byte_pair_ = str(byte_pairs_filtered[count_max_idx])
        byte_pair_ = str(byte_pairs_[index])

        print(f'byte_pair: {byte_pair_}', file=sys.stderr, flush=True)

        return byte_pair_

    else:
        return None


def replace_byte_pair(lines_, byte_pair_, NTC_idx_):
    # if len(lines_) % 2 != 0:
    #     lines_ = np.append(lines_, [' '])

    # print(f'line: {lines_}', file=sys.stderr, flush=True)
    # print(f'length: {len(lines_)}', file=sys.stderr, flush=True)

    idx = 0
    max_idx = len(lines_) - 1

    while idx < max_idx:

        # print(f'idx: {idx}', file=sys.stderr, flush=True)
        # print(f'equal_1: {lines_[idx] == byte_pair_[0]}', file=sys.stderr, flush=True)
        # print(f'equal_2: {lines_[idx + 1] == byte_pair_[1]}', file=sys.stderr, flush=True)

        if lines_[idx] == byte_pair_[0] and lines_[idx + 1] == byte_pair_[1]:

            # print(f'match index: {idx}', file=sys.stderr, flush=True)

            lines_[idx] = NON_TERMINAL_CHARS[NTC_idx_]
            lines_ = np.delete(lines_, idx + 1)
            max_idx = len(lines_) - 1

            # print(f'current_line: {lines_}', file=sys.stderr, flush=True)

            idx += 1
        else:
            idx += 1

    return lines_


NTC_idx = 0
prod_rules = {}

# byte_pairs = get_byte_pairs(lines)
# byte_pair = get_most_common_pair(byte_pairs)

print(f'line: {"".join(lines)}', file=sys.stderr, flush=True)

while True:

    byte_pairs = get_byte_pairs(lines)

    print(f'byte_pairs {NTC_idx}: {byte_pairs}', file=sys.stderr, flush=True)

    byte_pair = get_most_common_pair(byte_pairs)

    if byte_pair:

        prod_rules[NON_TERMINAL_CHARS[NTC_idx]] = byte_pair
        lines = replace_byte_pair(lines, byte_pair, NTC_idx)

        print(f'prod_rules: {prod_rules}', file=sys.stderr, flush=True)
        print(f'replaced_line {NTC_idx + 1}: {lines}', file=sys.stderr, flush=True)

        NTC_idx += 1

    else:
        break

print(''.join(lines).strip())
for rule in prod_rules:
    print(f'{rule} = {prod_rules[rule]}')
