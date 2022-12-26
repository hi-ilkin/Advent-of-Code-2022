import re


def get_monkeys():
    monkeys = {}
    lines = open('input.txt').readlines()
    for line in lines:
        k, v = line.strip().split(': ')

        if v.isnumeric():
            monkeys[k] = int(v)
        else:
            monkeys[k] = split_by_operation(v)

    # print(monkeys)
    return monkeys


def split_by_operation(operation_str):
    regex = r' ([+\-*/]) '
    return re.split(regex, operation_str)


def find_number(monkeys, key):
    if isinstance(monkeys[key], int):
        return monkeys[key]

    left, operation, right = monkeys[key]
    left_num = find_number(monkeys, left)
    right_num = find_number(monkeys, right)

    return eval(f'{left_num} {operation} {right_num}')


if __name__ == '__main__':
    ms = get_monkeys()
    print(find_number(ms, 'root'))
