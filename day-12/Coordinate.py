from dataclasses import dataclass


@dataclass
class Coordinate:
    row: int
    col: int
    distance: int = 0

    def __add__(self, coordinate):
        return Coordinate(self.row + coordinate.row, self.col + coordinate.col)

    def __lt__(self, other):
        return self.row < other.row or self.col < other.col

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def is_in_boudary(self, width, height):
        return 0 <= self.row < width and 0 <= self.col < height

    def __hash__(self):
        return self.row * 100 + self.col
