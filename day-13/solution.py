import numpy as np
import logging

logging.basicConfig(level=logging.WARNING, format='%(message)s')


def get_list(line):
    line = line[0].strip()
    return eval(line)


def is_order_correct(left, right):
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
            res = is_order_correct(li, ri)
            if res is not None:
                return res

    elif type_left == list and type_right == int:
        for li, ri in zip(left, [right]):
            res = is_order_correct(li, ri)
            if res is not None:
                return res

        return True if len(left) == 0 else False

    elif type_right == list and type_left == int:
        for li, ri in zip([left], right):
            res = is_order_correct(li, ri)
            if res is not None:
                return res

        return True if len(right) >= 1 else False

    if type(left) == type(right) == list:
        if len(left) == len(right):
            return None
        return len(left) < len(right)


def sort_packs(ordered_packets):
    for i in range(len(ordered_packets)):
        for j in range(0, len(ordered_packets) - i - 1):
            left = ordered_packets[j]
            right = ordered_packets[j + 1]
            if not is_order_correct(left, right):
                ordered_packets[j], ordered_packets[j + 1] = ordered_packets[j + 1], ordered_packets[j]

    return ordered_packets


def main():
    packets = []
    with open('input.txt') as fp:
        lines = fp.readlines()
        pair_count = 0
        packet_order_results = []
        for i in range(0, len(lines), 3):
            pair_count += 1
            left = get_list(lines[i: i + 1])
            right = get_list(lines[i + 1: i + 2])

            logging.debug(left)
            logging.debug(right)
            logging.debug('-' * 50)

            is_correct_order = is_order_correct(left, right)

            if is_correct_order:
                packets.append(left)
                packets.append(right)
            else:
                packets.append(right)
                packets.append(left)

            packet_order_results.append(is_correct_order)
            logging.debug(f'{pair_count}, {is_correct_order}')

            logging.debug('')

    logging.debug(packet_order_results)
    packet_order_results = np.array(packet_order_results)
    for i, res in enumerate(packet_order_results):
        logging.debug(f'{i + 1} {res}')

    logging.warning(f'Sum of the indices: {np.sum(packet_order_results * np.arange(1, len(packet_order_results) + 1))}')

    return packets


def solve_part_2(unordered_packets):
    unordered_packets.append([[2]])
    unordered_packets.append([[6]])

    ordered_packets = sort_packs(unordered_packets)
    result = 1
    for i, pack in enumerate(ordered_packets):
        if pack == [[2]] or pack == [[6]]:
            logging.error(f'Pack at {i + 1} {pack}')
            result *= (i + 1)

        logging.info(pack)
    logging.error(f'Result of part 2: {result}')


if __name__ == '__main__':
    _packets = main()
    solve_part_2(_packets)
