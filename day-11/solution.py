import logging

logging.basicConfig(level=logging.WARNING)

ROUNDS = 20


class Monkey:
    def __init__(self, items, operation, test_action, true_monkey_id, false_monkey_id):
        self.items = items
        self.old = items[0]
        self.operation = operation
        self.test_val = test_action
        self.true_monkey_id = true_monkey_id
        self.false_monkey_id = false_monkey_id
        self.items_inspected = 0

    def update_worry_level(self):
        return eval(self.operation) // 3

    def is_test_action_passed(self):
        return self.old % self.test_val == 0

    def increase_inspected_counter(self):
        self.items_inspected += len(self.items)


def parse_operation(operation):
    return operation.split('= ')[-1].replace('old', 'self.old').strip()


def parse_items(items):
    return list(map(int, (items.split(':')[-1]).split(',')))


def parse_test_value(value):
    return int(value.split('by')[-1])


def parse_condition(value):
    return int(value.split(' ')[-1])


def parse_input():
    monkeys = []
    with open('input.txt') as fp:
        while fp:
            line = fp.readline()
            if line == '':
                break
            line = line.strip()
            if line.startswith('Monkey'):
                starting_items = parse_items(fp.readline())
                operation = parse_operation(fp.readline())
                test = parse_test_value(fp.readline())
                true_condition_id = parse_condition(fp.readline())
                false_condition_id = parse_condition(fp.readline())

                m = Monkey(starting_items, operation, test, true_condition_id, false_condition_id)
                monkeys.append(m)
    return monkeys


def play(monkeys):
    for i, m in enumerate(monkeys):

        logging.debug(f'Monkey {i}:')
        m.increase_inspected_counter()
        for item in m.items:
            logging.debug(f'\tMonkey inspects an item with a worry level {item}')
            m.old = item
            m.old = m.update_worry_level()
            logging.debug(f'\tCurrent worry level: {m.old}')
            logging.debug(f'\t{m.old} is divisible by {m.test_val}? {m.old % m.test_val == 0}')
            if m.is_test_action_passed():
                logging.debug(f'\t\tYes, Send to {m.true_monkey_id}')
                monkeys[m.true_monkey_id].items.append(m.old)
            else:
                logging.debug(f'\t\tNo, Send to {m.false_monkey_id}')
                monkeys[m.false_monkey_id].items.append(m.old)
        m.items = []

    return monkeys


def main():
    monkeys = parse_input()
    for i in range(ROUNDS):
        if i % 100 == 0:
            logging.warning(f'Playing game {i}')
        monkeys = play(monkeys)

    monkeys = sorted(monkeys, key=lambda x: x.items_inspected, reverse=True)
    t1, t2 = monkeys[:2]
    logging.warning(f'Result:  {t1.items_inspected * t2.items_inspected}')


if __name__ == '__main__':
    main()
