import pytest

from solution import *


def test_path_parser():
    example_input = '10R5L5R10L4R5L5'
    expected_output = [10, 'R', 5, 'L', 5, 'R', 10, 'L', 4, 'R', 5, 'L', 5]
    actual = parse_directions(example_input)
    assert actual == expected_output


@pytest.mark.parametrize("cur_facing,direction,expected",
                         [(Facing.LEFT, 'R', Facing.UP), (Facing.LEFT, 'L', Facing.DOWN),
                          (Facing.UP, 'R', Facing.RIGHT), (Facing.UP, 'L', Facing.LEFT),
                          (Facing.RIGHT, 'R', Facing.DOWN), (Facing.RIGHT, 'L', Facing.UP),
                          (Facing.DOWN, 'R', Facing.LEFT), (Facing.DOWN, 'L', Facing.RIGHT)
                          ])
def test_facing(cur_facing, direction, expected):
    actual = change_facing(cur_facing, direction)

    assert expected == actual


def test_new_point_should_stay_on_same_x_if_orientation_not_changed():
    cur_point = (20, 50)

    expectec_new_point = (170, 0)
    new_point = calculate_new_point(cur_point, cur_section_id=1, next_section_id=6, new_facing=Facing.RIGHT, old_facing=Facing.RIGHT)
    assert expectec_new_point == new_point
