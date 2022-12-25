import re
from dataclasses import dataclass
from typing import List
import numpy as np
import matplotlib.pyplot as plt
from utils import timeit

IS_REAL_INPUT = True  # set false for part 1
Y_VALUE = 2_000_000 if IS_REAL_INPUT else 10

"""
Solution explained:
Distance to beacon is also the range of the sensor. Since Manhattan distance 
used to calculate distance, coverage area of a sensor is rectangle or 2 triangles
mirrored at y axis. Considering x,y as sensor point and r as range of the sensor,
3 points of the triangle would be: (x, y + r), (x + r, y), (x - r, y) where first 
point is top of the rectangle and remaining bottom. 

Part-1
Since requested row is known, it is enough to check the triangle facing to that line
and overlaps with it. Requested row cuts the triangles at two points and creates smaller 
triangle with head and cutting points. Height of this triangle is h=abs(row_y - head.y) 
and since this small triangle's inner angles are 45/45/90, bottom of this smaller triangle 
is 2*h. From here finding cutting points are easy: (head.x - h, y), (head.x + h, y).
Rest is easy, just keeping track of the cutting points, counting them and excluding beacons

Part-2
Similar logic with part-1, except all triangles are included and checking each row one by 
one and looking for empty cell at the end of each iteration. Execution time is extremely slow
since it check 4 million row. One possible optimization could be, first finding approximate
position by scaling everything down, then doing one-by-one check on that area.

"""


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
    coords_list = re.findall(r"-?\d+", input_string)
    return list(map(int, coords_list))


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


def generate_triangles(sensors):
    for sensor in sensors:
        x, y = sensor.point.x, sensor.point.y
        dist = sensor.range
        if sensor.is_facing_down():
            tr_y = y + dist
        else:
            tr_y = y - dist

        sensor.triangle = Triangle([Point(x - dist, y), Point(x + dist, y), Point(x, tr_y)])


def is_triangle_intersact_with_point(triangle, intersaction_point=Y_VALUE):
    top, bottom = triangle.get_head_bottom_point()
    if top.y <= intersaction_point <= bottom[0].y:
        return True

    if top.y >= intersaction_point >= bottom[0].y:
        return True

    return False


def draw_triangles(triangles):
    for tr in triangles:
        x_points = [p.x for p in tr.points]
        x_points.append(tr.points[0].x)

        y_points = [p.y for p in tr.points]
        y_points.append(tr.points[0].y)

        # plt.ylim([30, -10])
        plt.plot([-15 * 10 ** 5, 60 * 10 ** 5], [3835649, 3835649])
        plt.fill(x_points, y_points)
    plt.show()


def draw(sensors=None, mirror=False):
    for sensor in sensors:
        tr = sensor.triangle

        x_points = [p.x for p in tr.points]
        x_points.append(tr.points[0].x)

        y_points = [p.y for p in tr.points]
        y_points.append(tr.points[0].y)

        if mirror:
            head, bottom = tr.get_head_bottom_point()
            x_points.extend([head.x, bottom[0].x, bottom[1].x, head.x])
            y_points.extend([head.y - 2 * sensor.range, bottom[0].y, bottom[1].y, head.y - 2 * sensor.range])

        plt.ylim([30, -10])
        plt.plot([sensor.beacon.x], [sensor.beacon.y], 'o-')
        plt.fill(x_points, y_points)

    # plt.plot([-30**, 30], [10, 10])
    # plt.xlim([-1, 21])
    # plt.ylim([-1, 21])
    # plt.xticks(np.arange(-1, 21, 1))
    # plt.yticks(np.arange(-1, 21, 1))
    plt.grid(which='major', axis='y', zorder=-1.0)
    plt.grid(which='major', axis='x', zorder=-1.0)
    plt.show()


@timeit
def calculate_overlap(sensors, max_x, min_x):
    size = abs(max_x - min_x)
    row = np.zeros((size,), dtype=np.uint8)
    intersected_sensors = []
    for sensor in sensors:
        if is_triangle_intersact_with_point(sensor.triangle):
            head, _ = sensor.triangle.get_head_bottom_point()
            dif = abs(Y_VALUE - head.y)
            x1 = sensor.point.x - dif - min_x
            x2 = sensor.point.x + dif - min_x

            row[x1:x2 + 1] = 1
            intersected_sensors.append(sensor)

    for sensor in sensors:
        if sensor.beacon.y == Y_VALUE:
            row[sensor.beacon.x - min_x] = 0
    print(f'Number of non-beacon positions(overlapping triangles) {np.sum(row)}')


def get_upside_down(triangle, sensor_range):
    head, bottom = triangle.get_head_bottom_point()

    if head.y < bottom[0].y:
        return Triangle([Point(head.x, head.y + 2 * sensor_range), bottom[0], bottom[1]])
    else:
        return Triangle([Point(head.x, head.y - 2 * sensor_range), bottom[0], bottom[1]])


@timeit
def find_empty_cell(sensors):
    row_size = 4_000_000
    row_template = np.zeros((row_size,), dtype=np.uint8)
    row_counter = 3187704
    sensor_triangle_data = []
    trs_to_draw = []

    for sensor in sensors:
        triangles = [sensor.triangle, get_upside_down(sensor.triangle, sensor.range)]
        trs_to_draw.extend(triangles)
        sensor_triangle_data.append(([triangles, sensor.point.x]))

    # draw_triangles(trs_to_draw)

    while True:
        if row_counter % 10_000 == 0:
            print(f'Scanning row: {row_counter}')
        row = row_template.copy()
        for j, (triangles, sensor_x) in enumerate(sensor_triangle_data):
            for i, triangle in enumerate(triangles):
                if is_triangle_intersact_with_point(triangle, intersaction_point=row_counter):
                    head, _ = triangle.get_head_bottom_point()
                    dif = abs(row_counter - head.y)
                    x1 = sensor_x - dif
                    x2 = sensor_x + dif
                    x1 = max(0, x1)
                    x2 = min(x2, row_size)
                    row[x1:x2 + 1] = 1

        empty_row = np.where(row == 0)
        if len(empty_row[0]) != 0:
            break

        row_counter += 1

    print(f'Tuning frequency: {empty_row[0][0] * 4_000_000 + row_counter}')
    return row_counter, empty_row[0]


def main():
    all_sensors = parse_sensor_data()
    generate_triangles(all_sensors)

    max_x, min_x = get_x(all_sensors)
    print(f'Max/min x: {max_x}/{min_x}')
    # part 1
    calculate_overlap(all_sensors, max_x, min_x)

    # part 2
    print(find_empty_cell(all_sensors))
    # draw(all_sensors, mirror=True)


if __name__ == '__main__':
    main()
