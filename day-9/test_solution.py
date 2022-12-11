from solution import Rope, move_tail_v2


def assert_tail(expected_tail, tail):
    assert tail.x == expected_tail.x
    assert tail.y == expected_tail.y


def test_tail_should_move_up():
    head = Rope(x=1, y=4)
    tail = Rope(x=1, y=2)
    expected_tail = Rope(x=1, y=3)

    move_tail_v2(head, tail)
    assert_tail(expected_tail, tail)


def test_tail_should_move_left():
    head = Rope(x=1, y=2)
    tail = Rope(x=3, y=3)
    expected_tail = Rope(x=2, y=2)

    move_tail_v2(head, tail)
    assert_tail(expected_tail, tail)


def test_tail_should_move_right():
    head = Rope(x=3, y=2)
    tail = Rope(x=1, y=2)
    expected_tail = Rope(x=2, y=2)

    move_tail_v2(head, tail)
    assert tail.x == expected_tail.x
    assert tail.y == expected_tail.y


def test_tail_should_move_down():
    head = Rope(x=3, y=2)
    tail = Rope(x=3, y=4)
    expected_tail = Rope(x=3, y=3)

    move_tail_v2(head, tail)
    assert_tail(expected_tail, tail)


def test_tail_should_move_top_right():
    head = Rope(x=4, y=5)
    tail = Rope(x=3, y=3)
    expected_tail = Rope(x=4, y=4)

    move_tail_v2(head, tail)
    assert_tail(expected_tail, tail)


def test_tail_should_move_top_left():
    head = Rope(x=2, y=5)
    tail = Rope(x=3, y=3)
    expected_tail = Rope(x=2, y=4)

    move_tail_v2(head, tail)
    assert_tail(expected_tail, tail)


def test_tail_should_move_bottom_left():
    head = Rope(x=2, y=2)
    tail = Rope(x=3, y=4)
    expected_tail = Rope(x=2, y=3)

    move_tail_v2(head, tail)
    assert_tail(expected_tail, tail)


def test_tail_should_move_bottom_right():
    head = Rope(x=3, y=4)
    tail = Rope(x=2, y=6)
    expected_tail = Rope(x=3, y=5)

    move_tail_v2(head, tail)
    assert_tail(expected_tail, tail)
