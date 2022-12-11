# import numpy as np


def is_tree_visible_in_x_range(input_range, x, y, forest):
    steps = 0
    for v in input_range:
        steps += 1
        if forest[v][y] >= forest[x][y]:
            return False, steps
    return True, steps


def is_tree_visible_in_y_range(input_range, x, y, forest):
    steps = 0
    for v in input_range:
        steps += 1
        if forest[x][v] >= forest[x][y]:
            return False, steps
    return True, steps


def is_tree_visible(x, y, length, forest):
    inputs = [
        (is_tree_visible_in_x_range, range(x - 1, -1, -1)),
        (is_tree_visible_in_x_range, range(x + 1, length)),
        (is_tree_visible_in_y_range, range(y - 1, -1, -1)),
        (is_tree_visible_in_y_range, range(y + 1, length))
    ]

    visible: bool = False
    steps: int = 1
    for func, input_range in inputs:
        v, s = func(input_range, x, y, forest)
        visible = visible or v
        steps *= s

    return visible, steps * visible


def main():
    forest = read_input()

    visible_trees = 0
    length = len(forest)

    max_score = 0
    for x in range(length):
        for y in range(length):
            is_visible, scenic_score = is_tree_visible(x, y, length, forest)
            max_score = max(max_score, scenic_score)
            if is_visible:
                visible_trees += 1

    print(visible_trees)
    print(f'Max score: {max_score}')


def read_input():
    forest = []
    with open('input.txt') as fp:
        for line in fp.readlines():
            line = line.strip()
            forest.append(list(map(int, list(line))))

    # forest = np.array(forest)
    return forest


if __name__ == '__main__':
    main()
