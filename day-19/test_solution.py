from solution import *


def test_split_by_operation_should_return_sides():
    left = 'pppw'
    right = 'asdf'

    for op in ['+', '-', '*', '/']:
        operation = f'{left} {op} {right}'
        res = split_by_operation(operation)
        print('\n', res)
        actual_left, operation, actual_right = res

        assert actual_left == left
        assert actual_right == right
        assert op == operation
