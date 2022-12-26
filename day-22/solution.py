from enum import Enum

import numpy as np


class Facing(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


def complete_rows(array):
    max_row = 0
    for row in array:
        max_row = max(len(row), max_row)

    for row in array:
        row_len = len(row)
        if row_len < max_row:
            row.extend([2] * (max_row - row_len))

    return array


def get_inputs():
    mapped_board_map = []

    with open('input.txt') as fp:
        board_map, encoded_path = ''.join(fp.readlines()).split('\n\n')
        board_map = board_map.replace(' ', '2')
        board_map = board_map.replace('.', '0')
        board_map = board_map.replace('#', '1')

        for line in board_map.split('\n'):
            row = list(map(int, list(line)))
            mapped_board_map.append(row)

        mapped_board_map = complete_rows(mapped_board_map)
        mapped_board_map = np.array(mapped_board_map)
        # print(mapped_board_map)
        # print(encoded_path)

    return mapped_board_map, encoded_path.strip()


def find_start_point(board_map):
    row, col = np.where(board_map == 0)
    return row[0], col[0]


def parse_directions(direction_str):
    directions = []
    num = ''
    for s in direction_str:
        if s.isdigit():
            num += s
        else:
            if num != '':
                directions.append(int(num))

            directions.append(s)
            num = ''

    if num != '':
        directions.append(int(num))

    return directions


def get_move_dir(facing):
    if facing == Facing.LEFT:
        return 0, -1
    elif facing == Facing.RIGHT:
        return 0, 1
    elif facing == Facing.UP:
        return -1, 0
    elif facing == Facing.DOWN:
        return 1, 0


def wrap_around(cur_point, board_map, wrap_direction):
    height, width = board_map.shape
    x, y = cur_point
    if 0 <= x < height and 0 <= y < width and board_map[x][y] == 0:
        return x, y

    def _wrap_vertical():
        rows = np.where(board_map[:, y] != 2)
        nx = rows[0][0] if wrap_direction == Facing.DOWN else rows[0][-1]
        if board_map[nx][y] == 0:
            return nx, y
        return x, y

    def _wrap_horizontal():
        cols = np.where(board_map[x, :] != 2)
        ny = cols[0][0] if wrap_direction == Facing.RIGHT else cols[0][-1]
        if board_map[x][ny] == 0:
            return x, ny
        return x, y

    if wrap_direction == Facing.UP or wrap_direction == Facing.DOWN:
        if x < 0 or x >= height:
            return _wrap_vertical()

        elif board_map[x][y] == 2:
            return _wrap_vertical()

    else:
        if y < 0 or y >= width:
            return _wrap_horizontal()
        elif board_map[x][y] == 2:
            return _wrap_horizontal()

    return x, y


def get_current_section(cur_point):
    x, y = cur_point
    if 0 <= x < 50 and 50 <= y < 100:
        return 1
    elif 0 <= x < 50 and 100 <= y < 150:
        return 2
    elif 50 <= x < 100 and 50 <= y < 100:
        return 3
    elif 100 <= x < 150 and 50 <= y < 100:
        return 4
    elif 100 <= x < 150 and 0 <= y < 50:
        return 5
    elif 150 <= x < 200 and 0 <= y < 50:
        return 6
    raise Exception("Something is not correct")


def get_section_range(section):
    if section == 1:
        return (0, 50), (50, 100)
    elif section == 2:
        return (0, 50), (100, 150)
    elif section == 3:
        return (50, 100), (50, 100)
    elif section == 4:
        return (100, 150), (50, 100)
    elif section == 5:
        return (100, 150), (0, 50)
    elif section == 6:
        return (150, 200), (0, 50)


def get_next_section(wrap_direction, section_id):
    if section_id == 1:
        return {Facing.UP: (6, Facing.RIGHT), Facing.DOWN: (3, Facing.DOWN), Facing.RIGHT: (2, Facing.RIGHT), Facing.LEFT: (5, Facing.LEFT)}.get(wrap_direction)
    elif section_id == 2:
        return {Facing.UP: (6, Facing.UP), Facing.DOWN: (3, Facing.LEFT), Facing.RIGHT: (4, Facing.LEFT), Facing.LEFT: (1, Facing.LEFT)}.get(wrap_direction)
    elif section_id == 3:
        return {Facing.UP: (1, Facing.UP), Facing.DOWN: (4, Facing.DOWN), Facing.RIGHT: (2, Facing.UP), Facing.LEFT: (5, Facing.UP)}.get(wrap_direction)
    elif section_id == 4:
        return {Facing.UP: (3, Facing.UP), Facing.DOWN: (6, Facing.LEFT), Facing.RIGHT: (2, Facing.LEFT), Facing.LEFT: (5, Facing.LEFT)}.get(wrap_direction)
    elif section_id == 5:
        return {Facing.UP: (3, Facing.RIGHT), Facing.DOWN: (6, Facing.DOWN), Facing.RIGHT: (4, Facing.RIGHT), Facing.LEFT: (1, Facing.RIGHT)}.get(wrap_direction)
    elif section_id == 6:
        return {Facing.UP: (5, Facing.UP), Facing.DOWN: (2, Facing.DOWN), Facing.RIGHT: (4, Facing.UP), Facing.LEFT: (1, Facing.DOWN)}.get(wrap_direction)


def calculate_new_point(cur_point: tuple, cur_section_id: int, next_section_id: int, new_facing: Facing, old_facing: Facing) -> tuple:
    x, y = cur_point
    (nx_start, nx_end), (ny_start, ny_end) = get_section_range(next_section_id)
    (ox_start, ox_end), (oy_start, oy_end) = get_section_range(cur_section_id)

    # check if orientation changed
    if new_facing == old_facing:
        x = x - ox_start + nx_start
        y = y - oy_start + ny_start
    if new_facing.value % 2 == old_facing.value % 2:
        x = ox_end - x + nx_start
        y = oy_end - y + ny_start
    else:
        y = x - ox_start + ny_start
        x = y - oy_start + nx_start

    return x, y


def wrap_around_part_2(cur_point, board, wrap_direction):
    height, width = board.shape
    x, y = cur_point
    if 0 <= x < height and 0 <= y < width and board[x][y] != 2:
        return x, y

    dx, dy = get_move_dir(wrap_direction)
    section_id = get_current_section((x - dx, y - dy))
    next_section_id, new_facing = get_next_section(wrap_direction, section_id)
    nx, ny = calculate_new_point(cur_point, section_id, next_section_id, new_facing, wrap_direction)

    if board[nx][ny] == 0:
        return nx, ny
    else:
        return x, y

    # calculate new coordinates


def move_n_steps(cur_point, board_map, facing, n):
    display_map = board_map.copy()
    height, width = board_map.shape
    x, y = cur_point
    i = 0
    dx, dy = get_move_dir(facing)
    display_map[x][y] = 8
    nx, ny = wrap_around_part_2((x + dx, y + dy), board_map, facing)

    while 0 <= nx < height and 0 <= ny < width and board_map[nx][ny] == 0 and i < n:
        display_map[x][y] = 8
        x, y = nx, ny
        nx, ny = wrap_around_part_2((x + dx, y + dy), board_map, facing)
        i += 1

    return x, y


def change_facing(cur_facing, direction):
    if direction == 'R':
        d = 1
    else:
        d = -1

    return Facing((cur_facing.value + d) % 4)


def find_last_point(board_map, path):
    directions = parse_directions(path)
    start_point = find_start_point(board_map)
    facing = Facing.RIGHT

    print(f'Starting point: {start_point}')

    cur_point = start_point
    for i, d in enumerate(directions):
        if isinstance(d, int):
            try:
                cur_point = move_n_steps(cur_point, board_map, facing, d)
            except Exception as e:
                print(f'Problem at step {i}')
                print(e)
        else:
            facing = change_facing(facing, d)

    return cur_point, facing


def calcuate_password(point, facing):
    x, y = point
    return 1000 * (x + 1) + 4 * (y + 1) + facing.value


def main():
    board_map, path = get_inputs()
    last_point, last_facing = find_last_point(board_map, path)
    print(last_point, last_facing)
    print(f'Password is : {calcuate_password(last_point, last_facing)}')


if __name__ == '__main__':
    main()
