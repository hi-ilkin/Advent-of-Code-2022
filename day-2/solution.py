def part_1():
    value_points = {
        'X': 1,
        'Y': 2,
        'Z': 3
    }

    win_conditions = ['C X', 'A Y', 'B Z']
    draw_conditions = ['A X', 'B Y', 'C Z']
    total_score = 0

    with open('input.txt') as fp:
        for line in fp.readlines():
            game = line.strip()
            opponent, me = game.split()
            total_score += value_points[me]
            if game in draw_conditions:
                total_score += 3
            if game in win_conditions:
                total_score += 6

    print(total_score)


def part_2():
    """
    # X means you need to lose
    # Y means you need to end the round in a draw
    # Z means you need to win.

    A - rock beats scissors (3)
    B - paper beats rock (1)
    C - Scissors beat paper (2)
    """

    values = {
        'A X': 0 + 3,
        'B X': 0 + 1,
        'C X': 0 + 2,

        'A Y': 3 + 1,
        'B Y': 3 + 2,
        'C Y': 3 + 3,

        'A Z': 6 + 2,
        'B Z': 6 + 3,
        'C Z': 6 + 1,
    }

    total_score = 0
    with open('input.txt') as fp:
        for line in fp.readlines():
            game = line.strip()
            total_score += values[game]

    print(total_score)


if __name__ == '__main__':
    part_2()
