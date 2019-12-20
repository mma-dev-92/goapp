import unittest
from itertools import product
from random import choice, sample

from ...gologic.board.color import Color
from ...gologic.board.boardposition import BoardPosition


class BaseTestCaseClass(unittest.TestCase):
    def setUp(self):
        self.sizes = [9, 13, 19]
        self.coords = {size: self.__all_valid_coords(size) for size in self.sizes}
        self.boards = [BoardPosition(size) for size in self.sizes]

    def __all_valid_coords(self, size):
        return list(product(range(size), range(size)))

    def do_test_for_no_exception_rising(self, function, **params):
        try:
            function(**params)
        except Exception as error:
            self.fail("{} raised exception {} with parameters {}".format(
                function.__name__, error, kwargs_to_str(**params)))

    def __kwargs_to_str(self, **kwargs):
        return ' '.join(['{}={}'.format(param, kwargs[param]) for param in kwargs])

    def random_size_empty_board(self):
        return choice(self.boards)

    def random_coord(self, size):
        return choice(self.coords[size])

    def random_size(self):
        return choice(self.sizes)

    def fill(self, bp, coords):
        for color, coords in coords.items():
            for coord in coords:
                bp.set_field(coord, color)
        return bp

    def other_sizes(self, size):
        return [s for s in self.sizes if not s == size]

    def random_nonempty_board(self, non_empty_fields=50):
        random_size = self.random_size()
        return self.fill(BoardPosition(random_size), self.random_coords(
            random_size, non_empty_fields // 2, non_empty_fields // 2))

    def random_coords(self, size, black=5, white=5):
        rand_coords = sample(self.coords[size], black + white)
        return {
            Color.BLACK: rand_coords[:black],
            Color.WHITE: rand_coords[black:],
        }

    def empty_board(self, size):
        return BoardPosition(size)
