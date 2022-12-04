def parse_line(line):
    e1, e2 = line.strip().split(',')
    return map(int, e1.split('-')), map(int, e2.split('-'))


def part_2(lines):
    counter = 0

    for line in lines:
        (s1, s2), (s3, s4) = parse_line(line)
        cond = set(range(s1, s2 + 1)) & set(range(s3, s4 + 1))
        if cond:
            counter += 1

    return counter


def part_1(lines):
    counter = 0

    for line in lines:
        (s1, s2), (s3, s4) = parse_line(line)

        if s1 <= s3 and s2 >= s4:
            counter += 1
        elif s1 >= s3 and s2 <= s4:
            counter += 1

    return counter


if __name__ == '__main__':
    fp = open('input.txt')
    result = part_2(fp.readlines())
    print(result)
