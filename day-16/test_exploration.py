from exploration import *
import exploration


def test_should_return_weighted():
    exploration.rewards = {
        'a': 3,
        'b': 1,
        'c': 6,
        'd': 4
    }
    result = get_possible_future_rewards(list(exploration.rewards.keys()))
    expected = 1 * 1 + 2 * 3 + 3 * 4 + 4 * 6

    assert result == expected
