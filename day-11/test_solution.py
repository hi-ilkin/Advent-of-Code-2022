import solution


def test_should_parse_multiple_items_correctly():
    expected = [79, 98, 100]
    inpt_str = 'Starting items: 79, 98, 100'
    actual = solution.parse_items(inpt_str)
    assert expected == actual


def test_should_parse_single_item_correctly():
    expected = [79]
    inpt_str = 'Starting items: 79'
    actual = solution.parse_items(inpt_str)
    assert expected == actual


def test_parse_test_value_should_return_single_number():
    inpt_str = '  Test: divisible by 19'
    expected = 19
    actual = solution.parse_test_value(inpt_str)
    assert expected == actual


def test_parse_condition_should_return_single_number():
    inpt_str = '    If true: throw to monkey 1'
    expected = 1
    actual = solution.parse_condition(inpt_str)
    assert expected == actual
