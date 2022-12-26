import re
from sympy import sympify, solve, Symbol


def get_monkeys(is_part_2=False):
    monkeys = {}
    lines = open('input.txt').readlines()
    for line in lines:
        k, v = line.strip().split(': ')

        if v.isnumeric():
            if is_part_2 and k == 'humn':
                monkeys[k] = 'x'
            else:
                monkeys[k] = int(v)
        else:
            if is_part_2 and k == 'root':
                left, _, right = split_by_operation(v)
                monkeys[k] = [left, ',', right]
            else:
                monkeys[k] = split_by_operation(v)

    # print(monkeys)
    return monkeys


def split_by_operation(operation_str):
    regex = r' ([+\-*/]) '
    return re.split(regex, operation_str)


def find_number(monkeys, key):
    if isinstance(monkeys[key], int):
        print(f'{key}: {monkeys[key]}')
        return monkeys[key]
    #
    elif key == 'humn':
        return monkeys[key]

    left, operation, right = monkeys[key]
    left_num = find_number(monkeys, left)
    right_num = find_number(monkeys, right)
    # print(f'Monkey {key}, {left_num} {operation} {right_num}')

    return f'({left_num} {operation} {right_num})'


if __name__ == '__main__':
    is_part_2 = False
    ms = get_monkeys(is_part_2)
    equation = find_number(ms, 'root')

    if is_part_2:
        print(solve(sympify(f'Eq{equation}'), Symbol('x')))
    else:
        print(eval(equation))
