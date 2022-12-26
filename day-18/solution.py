import numpy as np


def part_1():
    faces = np.array([[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]])

    cubes = []
    for line in open('input.txt').readlines():
        str_xyz = line.strip().split(',')
        xyz = list(map(int, str_xyz))
        cubes.append(xyz)

    cubes = np.array(cubes)

    counter = 0
    for cube in cubes:
        for face in faces:
            if not np.any(np.all((cube + face) == cubes, axis=1)):
                counter += 1

    print(counter)


if __name__ == '__main__':
    part_1()
