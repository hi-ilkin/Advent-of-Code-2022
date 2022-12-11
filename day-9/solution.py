from dataclasses import dataclass, field


@dataclass
class Rope:
    x: int = 150
    y: int = 150
    visited_points: set = field(default_factory=set)


def move_head(head, direction, step):
    if direction == 'R':
        head.x += step
    elif direction == 'L':
        head.x -= step
    elif direction == 'U':
        head.y += step
    elif direction == 'D':
        head.y -= step


def move_tail_v2(head, tail):
    if abs(head.x - tail.x) == 2 and head.y == tail.y:
        tail.x += 1 if head.x - tail.x > 0 else -1
    elif abs(head.y - tail.y) == 2 and head.x == tail.x:
        tail.y += 1 if head.y - tail.y > 0 else -1
    elif head.x != tail.x and head.y != tail.y:
        tail.x += 1 if head.x - tail.x > 0 else -1
        tail.y += 1 if head.y - tail.y > 0 else -1

    tail.visited_points.add((tail.x, tail.y))


def move_tail(head, tail):

    dx = 1 if tail.x > head.x else -1
    dy = 1 if tail.y > head.y else -1

    if abs(head.x - tail.x) > 1 and abs(head.y - tail.y) > 1:
        tail.x += head.x - tail.x + dx
        tail.y += head.y - tail.y + dy

    if abs(head.x - tail.x) > 1 and abs(head.y - tail.y) >= 1:
        tail.x += head.x - tail.x + dx
        tail.y += head.y - tail.y

    if abs(head.x - tail.x) >= 1 and abs(head.y - tail.y) > 1:
        tail.x += head.x - tail.x
        tail.y += head.y - tail.y + dy

    if abs(head.x - tail.x) > 1:
        tail.x += head.x - tail.x + dx

    if abs(head.y - tail.y) > 1:
        tail.y += head.y - tail.y + dy

    tail.visited_points.add((tail.x, tail.y))


def main():
    lines = open('input.txt').readlines()
    head = Rope()
    knots = [Rope() for _ in range(1, 10)]

    for line in lines:
        line = line.strip()
        direction, step = line.split()
        for s in range(int(step)):
            move_head(head, direction, 1)
            # print(f'Step: {s}: head position: {head.x}, {head.y}, tail: {[(t.x, t.y) for t in knots]}')

            move_tail(head, knots[0])
            for i in range(len(knots) - 1):
                # print(f'\tKnot {i}, {i + 1}')
                move_tail(knots[i], knots[i + 1])

    print(len(knots[-1].visited_points))


if __name__ == '__main__':
    main()
