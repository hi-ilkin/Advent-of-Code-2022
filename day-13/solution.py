import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')


def get_list(line):
    line = line[0].strip()  # .replace('[', '').replace(']', '')
    # line = f'[{line}]'
    return eval(line)


def compare(left, right):
    type_left = type(left)
    type_right = type(right)

    logging.debug(f'Comparing: {left} and {right}')
    if type_left == int and type_right == int:
        if left == right:
            return None
        return left < right

    elif type_left == list and type_right == list:
        if len(left) == 0 and len(right) != 0:
            return True
        if len(right) == 0 and len(left) > 0:
            return False
        for li, ri in zip(left, right):
            res = compare(li, ri)
            if res is not None:
                return res

    elif type_left == list and type_right == int:
        for li, ri in zip(left, [right]):
            res = compare(li, ri)
            if res is not None:
                return res

        return True if len(left) == 0 else False

    elif type_right == list and type_left == int:
        for li, ri in zip([left], right):
            res = compare(li, ri)
            if res is not None:
                return res

        return True if len(right) >= 1 else False

    if type(left) == type(right) == list:
        if len(left) == len(right):
            return None
        return len(left) < len(right)


def main():
    with open('input.txt') as fp:
        lines = fp.readlines()
        pair_count = 0
        all_results = []
        for i in range(0, len(lines), 3):
            pair_count += 1
            left = get_list(lines[i: i + 1])
            right = get_list(lines[i + 1: i + 2])

            logging.debug(left)
            logging.debug(right)
            logging.debug('-' * 50)

            cmp = compare(left, right)
            all_results.append(cmp)
            logging.debug(f'{pair_count}, {cmp}')

            logging.debug('')

    logging.debug(all_results)
    all_results = np.array(all_results)
    for i, res in enumerate(all_results):
        logging.info(f'{i + 1} {res}')
    logging.warning(f'Sum of the indices: {np.sum(all_results * np.arange(1, len(all_results) + 1))}')


if __name__ == '__main__':
    main()
