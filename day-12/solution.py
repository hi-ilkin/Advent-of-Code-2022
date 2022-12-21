import numpy as np
from Coordinate import Coordinate

directions = [Coordinate(0, 1), Coordinate(0, -1), Coordinate(1, 0), Coordinate(-1, 0)]
grid = []

original_start = None
width, height = None, None
end = None


def get_height(loc):
    if loc.islower():
        return ord(loc) - 97
    return ord('a') - 97 if loc == 'S' else ord('z') - 97


def generate_map():
    global grid, end, width, height, original_start
    lines = open('input.txt').readlines()

    for x, line in enumerate(lines):
        row = []
        for y, cell in enumerate(list(line.strip())):
            if cell == 'S':
                original_start = Coordinate(x, y)
            elif cell == 'E':
                end = Coordinate(x, y)
            row.append(get_height(cell))
        grid.append(row)

    print(f'Original start: {original_start}, End: {end}')
    heatmap = np.array(grid)
    width, height = heatmap.shape


def get_possible_starts():
    _grid = np.array(grid)
    possible_starts = [Coordinate(x, y) for x, y in zip(*np.where(_grid == 0))]
    return possible_starts


def find_shortest_path_distance(s):
    cur_position = s

    visited = np.zeros(np.array(grid).shape)

    queue = [cur_position]
    visited[cur_position.row][cur_position.col] = True
    while len(queue) != 0:
        cur_position = queue.pop(0)

        if cur_position == end:
            return cur_position.distance

        moves = get_valid_moves(cur_position, visited)
        for move in moves:
            queue.append(move)

    return 99999999


def is_valid(cur_position, new_position):
    return grid[new_position.row][new_position.col] - grid[cur_position.row][cur_position.col] <= 1


def get_valid_moves(cur_position, visited):
    moves = []
    for d in directions:
        tmp_position = cur_position + d
        tmp_position.distance = cur_position.distance + 1
        if tmp_position.is_in_boudary(width, height) \
                and is_valid(cur_position, tmp_position) \
                and not visited[tmp_position.row][tmp_position.col]:
            visited[tmp_position.row][tmp_position.col] = True
            moves.append(tmp_position)
    return moves


if __name__ == '__main__':
    generate_map()
    starts = get_possible_starts()

    print(f'Shortest path with original input: {find_shortest_path_distance(original_start)}')

    min_distance = 999999
    for start in starts:
        dist = find_shortest_path_distance(start)
        min_distance = min(dist, min_distance)

    print(f'Shortest path dist: {min_distance}')

