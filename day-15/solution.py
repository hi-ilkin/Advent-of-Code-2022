import re
from dataclasses import dataclass
from typing import List
import numpy as np
import matplotlib.pyplot as plt
from utils import timeit


IS_REAL_INPUT = True
Y_VALUE = 2_000_000 if IS_REAL_INPUT else 10


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Triangle:
    points: List[Point]

    def get_head_bottom_point(self):
        p1, p2, p3 = self.points
        if p1.y == p2.y:
            return p3, (p1, p2)
        elif p2.y == p3.y:
            return p1, (p2, p3)
        return p2, (p1, p3)


class Sensor:
    def __init__(self, x, y, b_x, b_y):
        self.point = Point(x, y)
        self.beacon = Point(b_x, b_y)
        self.range = get_manhattan_dist(self.point, self.beacon)
        self.triangle = None

    def is_facing_down(self):
        return self.point.y < Y_VALUE

    def __str__(self):
        return f'Sensor ({self.point}): closest beacon: {self.beacon} range: {self.range}: triangle: {self.triangle}'


def get_manhattan_dist(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def get_coords(input_string):
    coords_list = re.findall(r"\d+", input_string)
    return list(map(int, coords_list))


@timeit
def parse_sensor_data():
    sensors = []
    with open('input.txt') as fp:
        for line in fp.readlines():
            sensors.append(Sensor(*get_coords(line)))
    return sensors


def get_x(sensors):
    max_x = []
    for sensor in sensors:
        max_x.extend(sorted([p.x for p in sensor.triangle.points]))
    max_x = sorted(max_x)
    return max_x[-1], max_x[0]


@timeit
def generate_triangles(sensors):
    for sensor in sensors:
        x, y = sensor.point.x, sensor.point.y
        dist = sensor.range
        if sensor.is_facing_down():
            tr_y = y + dist
        else:
            tr_y = y - dist

        sensor.triangle = Triangle([Point(x - dist, y), Point(x + dist, y), Point(x, tr_y)])


def is_triangle_intersact_with_point(triangle):
    top, bottom = triangle.get_head_bottom_point()
    if top.y < Y_VALUE < bottom[0].y:
        return True

    if top.y > Y_VALUE > bottom[0].y:
        return True

    return False


def draw(sensors):
    for sensor in sensors:
        tr = sensor.triangle

        x_points = [p.x for p in tr.points]
        x_points.append(tr.points[0].x)

        y_points = [p.y for p in tr.points]
        y_points.append(tr.points[0].y)

        plt.plot(x_points, y_points)

    plt.plot([-30, 30], [10, 10])
    # plt.xlim([-10, 30])
    # plt.ylim([-10, 30])
    # plt.xticks(np.arange(-30, 30, 2))
    # plt.yticks(np.arange(-30, 30, 2))
    plt.grid(which='major', axis='y', zorder=-1.0)
    plt.grid(which='major', axis='x', zorder=-1.0)
    plt.show()


@timeit
def calculate_overlap(sensors, ma_x, mi_x):
    size = abs(ma_x - mi_x)
    row = np.full((size,), 0, dtype=np.uint8)
    intersected_sensors = []
    for sensor in sensors:
        if is_triangle_intersact_with_point(sensor.triangle):
            head, _ = sensor.triangle.get_head_bottom_point()
            dif = abs(Y_VALUE - head.y)
            x1 = sensor.point.x - dif - min_x
            x2 = sensor.point.x + dif - min_x

            print(f'Head: {head}, dif: {dif}, x1: {x1}, x2: {x2}')
            row[x1:x2 + 1] = 1
            intersected_sensors.append(sensor)

    for sensor in sensors:
        if sensor.beacon.y == Y_VALUE:
            print(f'Removing item : {sensor.beacon.x - min_x}')
            row[sensor.beacon.x - min_x] = 0
    # draw(intersected_sensors)
    print(np.sum(row))


if __name__ == '__main__':
    all_sensors = parse_sensor_data()
    generate_triangles(all_sensors)

    max_x, min_x = get_x(all_sensors)
    print(f'Max/min x: {max_x}/{min_x}')
    calculate_overlap(all_sensors, max_x, min_x)
    # 4878700
