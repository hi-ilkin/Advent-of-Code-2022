import logging

logging.basicConfig(level=logging.INFO)


def get_point(ch):
    return ord(ch) - 96 if ch.islower() else ord(ch) - 38


def part_1(fp):
    total_points = 0

    for line in fp.readlines():
        line = line.strip()
        l = len(line)
        c1, c2 = line[:l // 2], line[l // 2:]

        common_items = list(set(c1) & set(c2))
        c = common_items[0]
        logging.info(c1, c2, c, ord(c), get_point(c))
        total_points += get_point(c)

    return total_points


def part_2(fp):
    total_points = 0
    lines = fp.readlines()
    s = 0
    for i in range(3, len(lines) + 1, 3):
        c1, c2, c3 = list(map(str.strip, lines[s:i]))
        common_item = list(set(c1) & set(c2) & set(c3))[0]
        total_points += get_point(common_item[0])

        s += 3
    return total_points


if __name__ == '__main__':
    _fp = open('input.txt')
    _total_points = part_2(_fp)
    logging.warning(_total_points)
