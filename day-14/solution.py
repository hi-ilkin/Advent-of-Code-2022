import cv2
import numpy as np
from CaveMapper import generate_cave_map
from utils import timeit

SAND = 1
AIR = 0
ROCK = -1
START = 2

cave = generate_cave_map()
source = list(zip(*np.where(cave == START)))[0]
width, height = cave.shape


@timeit
def main():
    sand_count = 0
    while True:
        cur_col = cave[:, source[1]]
        items = np.where(cur_col != AIR)[0]
        last_air_position = (items[1] - 1, source[1])

        # print(f'Last_sand_position: {last_air_position}')

        last_sand_position = move_sand(last_air_position)
        if last_sand_position is None:
            break
        cave[last_sand_position] = SAND
        sand_count += 1
    print(f'Number of sands rested: {sand_count}')
    cv2.imwrite('cave.png', cv2.resize(cave*50, dsize=(0, 0), fx=8, fy=8))


def move_sand(available_pos):
    x, y = available_pos
    is_sand_rested = False
    is_moved = False

    while not is_sand_rested:
        if x < 0 or x >= width or y < 0 or y >= height:
            return None

        if cave[x + 1][y] == AIR:
            x += 1
        elif cave[x + 1][y - 1] == AIR:
            y -= 1
            x += 1
        elif cave[x + 1][y + 1] == AIR:
            y += 1
            x += 1
        else:
            is_sand_rested = True

    return x, y


if __name__ == '__main__':
    main()
