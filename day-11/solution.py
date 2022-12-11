class Monkey:
    def __init__(self, items, operation, test_action, true_monkey_id, false_monkey_id):
        self.items = items
        self.old = items[0]
        self.operation = operation
        self.test_action = test_action
        self.true_monkey_id = true_monkey_id
        self.false_monkey_id = false_monkey_id

    def apply_operation(self):
        return eval(self.operation)


def parse_operation(operation):
    return operation.split('= ')[-1].replace('old', 'self.old')


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


def main():
    monkeys = parse_input()
    for i, m in enumerate(monkeys):
        print(i, m.items, m.operation, m.apply_operation())


if __name__ == '__main__':
    main()
