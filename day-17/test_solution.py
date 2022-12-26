import pytest

from solution import *


@pytest.mark.parametrize("figure", [VERTICAL_LINE, HORIZONTAL_LINE, SQUARE, PLUS, FLIPPED_L])
def test_collision_when_reaced_bottom(figure):
    cave = np.zeros((7, 10), dtype=np.uint8)
    figure.current_index = (6, 0)
    assert is_collision(cave, figure)


def test_no_collision_when_items_not_allign():
    figure = VERTICAL_LINE
    figure.current_index = (4, 6)
    cave = np.ones((20, 7), dtype=np.uint8)
    cave[0:15, -1] = 0

    assert not is_collision(cave, figure)


def test_collision_with_plus():
    pass


def test_settle_rocks():
    plus = PLUS
    cave = np.zeros((10, 7), dtype=np.uint8)
    plus.current_index = (3, 4)

    vl = VERTICAL_LINE
    vl.current_index = (7, 0)

    square = SQUARE
    square.current_index = (4, 3)

    settle_rock(cave, plus)
    settle_rock(cave, vl)
    settle_rock(cave, square)

    expected_cave = np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 1, 1, 1, 0],
        [1, 0, 0, 1, 1, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ])

    assert np.all(expected_cave == cave)


def test_settle_horizontal_line():
    hl = HORIZONTAL_LINE
    cave = np.zeros((10, 7), dtype=np.uint8)
    hl.current_index = (2, 1)
    expected_cave = np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ])

    setteled_cave = settle_rock(cave, hl)
    print('\n', setteled_cave)
    assert np.all(expected_cave == cave)


def test_action_generator_creates_with_correct_order():
    actions = list('>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>')
    act_generator = get_next_input()

    for i, (action, actual) in enumerate(zip(actions, act_generator)):
        expected_dir = 1 if action == '>' else -1
        assert expected_dir == actual, f'Item {i} is not correct: {action}'
