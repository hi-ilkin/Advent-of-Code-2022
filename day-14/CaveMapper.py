import numpy as np
import cv2
from elements import *


def get_edge_points(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    start_x = min(x1, x2)
    end_x = max(x1, x2)
    start_y = min(y1, y2)
    end_y = max(y1, y2)

    return start_x, end_x, start_y, end_y


def generate_cave_map(add_floor=False):
    rock_lines = []
    max_x = 0
    min_x = 0
    max_y = 0
    min_y = np.inf

    for line in open('input.txt').readlines():
        points = line.strip().split('->')
        points = np.array([list(map(int, p.split(','))) for p in points])
        max_x = max(max_x, np.max(points[:, 1]))

        max_y = max(max_y, np.max(points[:, 0]))
        min_y = min(min_y, np.min(points[:, 0]))

        rock_lines.append(np.array(points))

    height = max_x - min_x + 1
    width = max_y - min_y + 1
    print(f'Width: {width} height: {height}')

    generated_cave_map = np.zeros((height, width), dtype=np.uint8)
    generated_cave_map[0][500 - min_y] = START
    # subtract min_x from x values and min_y from y values to normalize the table
    for rock_line in rock_lines:
        rock_line[:, 0] = rock_line[:, 0] - min_y

        for i in range(len(rock_line) - 1):
            start_x, end_x, start_y, end_y = get_edge_points(rock_line[i], rock_line[i + 1])
            generated_cave_map[start_y:end_y + 1, start_x:end_x + 1] = ROCK

    if add_floor:
        generated_cave_map = np.vstack(
            (generated_cave_map, np.zeros((1, width), dtype=np.uint8), np.ones((1, width), dtype=np.uint8) * ROCK))

    cv2.imwrite('cave.png', cv2.resize(generated_cave_map * 10, dsize=(0, 0), fx=8, fy=8))
    return generated_cave_map
