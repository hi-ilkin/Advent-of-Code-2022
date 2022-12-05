"""
Because I'm too lazy to parse stack input,
I created it manually and read rest of the input from file :)
"""
stacks = {
    1: list('GFVHPS'),
    2: list('GJFBVDZM'),
    3: list('GMLJN'),
    4: list('NGZVDWP'),
    5: list('VRCB'),
    6: list('VRSMPWLZ'),
    7: list('THP'),
    8: list('QRSNCHZV'),
    9: list('FLGPVQJ')
}


def pop_n(stack_id: int, n: int, flip=True) -> list:
    stack = stacks[stack_id]
    items = stack[-n:][::-1] if flip else stack[-n:]
    del stack[-n:]
    stacks[stack_id] = stack
    return items


def move_crates(lines: iter, is_part_1: bool):
    for line in lines:
        count, from_stack, to_stack = map(int, line.strip().split(' ')[1::2])
        stacks[to_stack].extend(pop_n(from_stack, count, is_part_1))

    print(''.join([x[-1] for x in stacks.values()]))


if __name__ == '__main__':
    _lines = open('input.txt').readlines()
    # move_crates(_lines, is_part_1=True)
    move_crates(_lines, is_part_1=False)
