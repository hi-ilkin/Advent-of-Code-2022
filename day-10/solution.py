import numpy as np

important_cycles = [20, 60, 100, 140, 180, 220]


def print_scr(screen, sprt, crt_x, crt_y):
    print(f'CRT draws pixel in position {sprt}')
    print(f'Sprite position: {crt_x} {crt_y}')
    print()

    if crt_y - 1 <= sprt <= crt_y + 1:
        screen[crt_x][crt_y] = 1


def get_coordinates(cycle):
    row = cycle // 40
    col = cycle - row * 40
    return row, col


def part_2():
    fp = open('input.txt')
    screen = np.zeros((6, 40))
    cycle = 0
    sprite_pos = 1
    for line in fp.readlines():
        row, col = get_coordinates(cycle)
        line = line.strip()

        print_scr(screen, sprite_pos, row, col)

        if line == 'noop':
            cycle += 1
        else:
            row, col = get_coordinates(cycle + 1)
            print_scr(screen, sprite_pos, row, col)

            val = int(line.split()[-1])
            sprite_pos += val
            cycle += 2

    screen = screen.reshape(6, 40)
    for row in screen:
        for item in row:
            print(' . ' if item == 0 else ' # ', end='')
        print()


def main():
    signal_strength = 0
    fp = open('input.txt')

    cycle = 0
    x = 1
    val = 0

    for important_cycle in important_cycles:
        while cycle < important_cycle:
            line = fp.readline().strip()
            if line == 'noop':
                cycle += 1
                val = 0

            else:
                cur_action, val = line.split(' ')
                val = int(val)
                cycle += 2
                x += val

        if cycle != important_cycle:
            tc = (cycle - 1)
            tx = (x - val)
        elif cycle == important_cycle and cur_action != 'noop':
            tx = (x - val)
            tc = cycle
        else:
            tc = cycle
            tx = x

        print(f'Cycle: {tc} * {tx} = {tc * tx}')

        signal_strength += tc * tx
    print(signal_strength)


if __name__ == '__main__':
    part_2()
