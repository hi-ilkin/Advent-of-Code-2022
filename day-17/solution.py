import cv2

from shapes import *

import numpy as np
from typing import List

chamber = np.zeros((4000, 7), dtype=np.uint8)

height, width = chamber.shape
print(height, width)
print(chamber)

actions = list(open('input.txt').readlines()[0].strip())


def is_collision(chamber_map: np.ndarray, rock: Shape):
    height, width = chamber_map.shape
    rock_x, rock_y = rock.current_index
    x_indices = []
    y_indices = []

    for x, y in rock.check_indexes:
        if 0 <= y + rock_y < width:
            x_indices.append(x + rock_x)
            y_indices.append(y + rock_y)

    x_indices = np.array(x_indices)
    y_indices = np.array(y_indices)
    if np.any(x_indices >= height):
        return True

    check_area = chamber_map[x_indices, y_indices]
    return np.any(check_area > 0)


def settle_rock(chamber_map: np.ndarray, rock: Shape):
    x, y = rock.current_index
    h, w = rock.shape.shape

    chamber_map[x - h + 1:x + 1, y:y + w] = np.logical_or(chamber_map[x - h + 1:x + 1, y:y + w], rock.shape)


def move_rock(rock: Shape, direction: int):
    cur_index = rock.current_index
    h, w = rock.shape.shape
    x, y = cur_index
    new_x, new_y = x, y + direction
    if 0 <= new_y and new_y + w <= width and np.all(chamber[x - h + 1:x + 1, new_y:new_y + w + 1] == 0):
        rock.current_index = (new_x, new_y)


def visualize_map(rock=None, i=0):
    img = chamber.copy()

    if rock:
        h, w = rock.shape.shape
        x, y = rock.current_index
        img[x - h:x, y: y + w] = rock.shape

    img = img[height - 50 - i: height - i, :]
    cv2.imshow('frame', cv2.resize(img * 255, dsize=(0, 0), fx=20, fy=20, interpolation=cv2.INTER_CUBIC))
    cv2.waitKey()


def print_map():
    tmp = chamber.copy().astype('object')
    tmp[tmp == 0] = '.'
    tmp[tmp == 1] = '#'
    print(tmp)


def play_game(n_times=1):
    action_generator = get_next_input()
    shape_generator = get_next_shape()
    last_x = height - 3
    action = next(action_generator)

    for i in range(n_times):
        rock_is_setteled = False
        rock = next(shape_generator)
        rock.current_index = (last_x - 1, 2)

        while not rock_is_setteled:
            visualize_map(rock, 2* i // 5)
            move_rock(rock, direction=action)
            visualize_map(rock, 2 * i // 5)
            if not is_collision(chamber, rock):
                rock.move_down()
            else:
                rock_is_setteled = True
                settle_rock(chamber, rock)
                last_x = get_tallest_point() - 3

            action = next(action_generator)

    print_map()
    # visualize_map()


def get_next_input():
    cur_action = 0

    while True:
        yield 1 if actions[cur_action % len(actions)] == '>' else -1
        cur_action += 1


def get_next_shape():
    shapes: List[Shape] = [HORIZONTAL_LINE, PLUS, FLIPPED_L, VERTICAL_LINE, SQUARE]
    cur_action = 0
    while True:
        yield shapes[cur_action % len(shapes)]
        cur_action += 1


def get_tallest_point():
    rock_points = np.where(chamber != 0)[0]
    return rock_points[0]


def main():
    play_game(2022)
    tallest_point = height - get_tallest_point()
    print(f'Tallest point: {tallest_point}')
    return tallest_point


if __name__ == '__main__':
    main()
