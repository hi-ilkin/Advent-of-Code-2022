from enum import Enum

import cv2
import numpy as np
from CaveMapper import generate_cave_map
from utils import timeit
from elements import *


EXPANSION_SIZE = 50


class Sand(Enum):
    SETTELED = 0
    OVERFLOW_LEFT = 1
    OVERFLOW_RIGHT = 2
    SOURCE_BLOCKED = 3


@timeit
def main(is_part_1=True):
    global cave, source, width
    sand_count = 0
    while True:
        cur_col = cave[:, source[1]]
        items = np.where(cur_col != AIR)[0]
        last_air_position = (items[1] - 1, source[1])

        # print(f'Last_sand_position: {last_air_position}')
        last_sand_position, status = move_sand(last_air_position)

        if is_part_1 and status in (Sand.OVERFLOW_LEFT, Sand.OVERFLOW_RIGHT):
            break

        if status == Sand.SOURCE_BLOCKED:
            sand_count += 1
            break
        elif status == Sand.SETTELED:
            cave[last_sand_position] = SAND
            sand_count += 1
        elif status == Sand.OVERFLOW_LEFT:
            cave = np.hstack((np.zeros((height, EXPANSION_SIZE), dtype=np.uint8), cave))
            cave[-1, :] = ROCK
            source = (source[0], source[1] + EXPANSION_SIZE)
            width += EXPANSION_SIZE
        elif status == Sand.OVERFLOW_RIGHT:
            cave = np.hstack((cave, np.zeros((height, EXPANSION_SIZE), dtype=np.uint8)))
            cave[-1, :] = ROCK
            width += EXPANSION_SIZE

    print(f'{"Part 1:" if is_part_1 else "Part 2:"} Number of sands rested: {sand_count}')


def move_sand(available_pos):
    x, y = available_pos
    is_sand_rested = False

    while not is_sand_rested:
        if y >= (width - 1):
            return None, Sand.OVERFLOW_RIGHT
        elif y < 0:
            return None, Sand.OVERFLOW_LEFT

        if cave[x + 1][y] == AIR:
            x += 1
        elif cave[x + 1][y - 1] == AIR:
            y -= 1
            x += 1
        elif cave[x + 1][y + 1] == AIR:
            y += 1
            x += 1
        else:
            if x == source[0] and y == source[1]:
                return None, Sand.SOURCE_BLOCKED
            is_sand_rested = True

    return (x, y), Sand.SETTELED


if __name__ == '__main__':
    cave = generate_cave_map(add_floor=False)
    source = list(zip(*np.where(cave == START)))[0]
    height, width = cave.shape
    main(is_part_1=True)
    main(is_part_1=False)
