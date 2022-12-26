from dataclasses import dataclass
import numpy as np


@dataclass
class Shape:
    """
    Left bottom corner of the shape is (0,0) point
    check_indexes indicates which indexes should be evaluated
    relative to (0,0) point to find out collision.

    """
    name: str
    shape: np.ndarray
    check_indexes: np.ndarray
    current_index: tuple = None

    def move_down(self):
        self.current_index = (self.current_index[0] + 1, self.current_index[1])


HORIZONTAL_LINE = Shape('horizontal_line', np.array([[1, 1, 1, 1]], dtype=np.uint8),
                        np.array([[1, 0], [1, 1], [1, 2], [1, 3]]))

PLUS = Shape('plus', np.array([
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
], dtype=np.uint8), np.array([[0, 0], [1, 1], [0, 2]]))

FLIPPED_L = Shape('flipped_l', np.array([
    [0, 0, 1],
    [0, 0, 1],
    [1, 1, 1]
], dtype=np.uint8), np.array([[1, 0], [1, 1], [1, 2]]))

VERTICAL_LINE = Shape('vertical_line', np.array([
    [1],
    [1],
    [1],
    [1]
], dtype=np.uint8), np.array([[1, 0]]))

SQUARE = Shape('square', np.array([
    [1, 1],
    [1, 1]
], dtype=np.uint8), np.array([[1, 0], [1, 1]]))
