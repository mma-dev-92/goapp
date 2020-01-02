import unittest
import colorama
from itertools import product
from random import choice, sample
from termcolor import colored

from gologic.board.color import Color
from gologic.board.boardposition import BoardPosition


class BaseTestCaseClass(unittest.TestCase):
    def setUp(self):
        self.sizes = [9, 13, 19]
        self.coords = {size: self.__all_valid_coords(size) for size in self.sizes}
        self.boards = [BoardPosition(size) for size in self.sizes]

    def __all_valid_coords(self, size):
        return list(product(range(size), range(size)))

    def print_position(self, bp):
        return '\n'.join([self.print_bp_row(bp, row) for row in range(bp.size)])

    def print_bp_row(self, bp, row):
        return ''.join([self.print_field(bp.at((row, col))) for col in range(bp.size)])

    def print_field(self, field):
        return self.print_nonempty_field(field) if not field.is_empty() else self.print_empty_field()

    def print_empty_field(self):
        return colored('+', 'yellow', 'on_cyan', attrs=['blink'])

    def print_nonempty_field(self, field):
        return colored('o', 'grey', 'on_cyan', attrs=['blink']) if field.is_black() else colored(
            'o', 'white', 'on_cyan', attrs=['blink'])

    def error_msg(self, bp, input, result, expected_result):
        return "\n\nError on board:\n{}\n{}\n{}\ninput: {}\noutput is: {}\nbut should be: {}".format(
            bp.size * "-", self.print_position(bp), bp.size * "-", input, result, expected_result)

    def do_test_for_no_exception_rising(self, function, **params):
        try:
            function(**params)
        except Exception as error:
            self.fail("{} raised exception {} with parameters {}".format(
                function.__name__, error, kwargs_to_str(**params)))

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
