important_cycles = [20, 60, 100, 140, 180, 220]


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

        print(f'Cycle: {tc} * {tx} = {tc*tx}')

        signal_strength += tc*tx
    print(signal_strength)


if __name__ == '__main__':
    main()
