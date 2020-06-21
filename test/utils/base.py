import unittest
from itertools import product
from random import choice, sample
from termcolor import colored

from gologic.board.color import Color
from gologic.board.boardposition import BoardPosition


class BaseTestCaseClass(unittest.TestCase):
    def setUp(self):
        self.sizes = [9, 13, 19]
        self.coordinates = {size: self.__all_valid_coordinates(size) for size in self.sizes}
        self.boards = [BoardPosition(size) for size in self.sizes]

    @staticmethod
    def __all_valid_coordinates(size):
        return list(product(range(size), range(size)))

    def print_position(self, bp):
        return '\n'.join(
            [self.print_bp_row(bp, row) for row in range(bp.size)])

    def print_bp_row(self, bp, row):
        return ''.join(
            [self.print_field(bp.at((row, col))) for col in range(bp.size)])

    def print_field(self, field):
        return self.print_nonempty_field(field) if not field.is_empty() else self.print_empty_field()

    @staticmethod
    def print_empty_field():
        return colored('+', 'yellow', 'on_cyan', attrs=['blink'])

    @staticmethod
    def print_nonempty_field(field):
        return colored('o', 'grey', 'on_cyan', attrs=['blink']) if field.is_white() else colored(
            'o', 'white', 'on_cyan', attrs=['blink'])

    def error_msg(self, bp, input_data, result, expected_result):
        return "\n\nError on board:\n{}\n{}\n{}\ninput: {}\noutput is: \n{}\nbut should be: \n{}".format(
            bp.size * "-", self.print_position(bp), bp.size * "-", input_data, result, expected_result)

    def do_test_for_no_exception_rising(self, function, **params):
        try:
            function(**params)
        except Exception as error:
            self.fail("{} raised exception {}".format(
                function.__name__, error))

    def random_size_empty_board(self):
        return choice(self.boards)

    def random_coord(self, size):
        return choice(self.coordinates[size])

    def random_size(self):
        return choice(self.sizes)

    @staticmethod
    def fill(bp, coordinates):
        for color, coordinates in coordinates.items():
            for coord in coordinates:
                bp.set_field(coord, color)
        return bp

    def other_sizes(self, size):
        return [s for s in self.sizes if not s == size]

    def random_nonempty_board(self, non_empty_fields=50):
        random_size = self.random_size()
        return self.fill(BoardPosition(random_size), self.random_coordinates(
            random_size, non_empty_fields // 2, non_empty_fields // 2))

    def random_coordinates(self, size, black=5, white=5):
        rand_coordinates = sample(self.coordinates[size], black + white)
        return {
            Color.BLACK: rand_coordinates[:black],
            Color.WHITE: rand_coordinates[black:],
        }

    @staticmethod
    def empty_board(size):
        return BoardPosition(size)

    @staticmethod
    def random_color():
        return choice([Color.BLACK, Color.WHITE])

    @staticmethod
    def alter_board_conf(conf, to_remove, to_add):
        for color, coordinates in to_add.items():
            for coordinate in coordinates:
                if coordinate not in conf[color]:
                    conf[color].append(coordinate)

        for color, coordinates in to_remove.items():
            for coordinate in coordinates:
                if coordinate in conf[color]:
                    conf[color].remove(coordinate)

        return conf

    @staticmethod
    def two_colors_coordinates():
        return {
            Color.BLACK: [(2, 0), (1, 1), (0, 2), (1, 2), (1, 4), (2, 4), (2, 3), (2, 5), (3, 4)],
            Color.WHITE: [(1, 0), (0, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3)]
        }

    @staticmethod
    def simple_board_position():
        return {
            Color.BLACK: [
                (6, 2), (7, 2), (6, 1), (2, 0), (1, 4), (2, 4), (3, 4), (2, 3), (2, 5)
            ],
            Color.WHITE: [
                (0, 1), (1, 0), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3)
            ]
        }

    @staticmethod
    def diagonal_stones_one_color_position():
        return {
            Color.BLACK: [
                (0, 0), (0, 2), (2, 0), (1, 1)
            ]
        }

    @staticmethod
    def diagonal_stones_both_color_position():
        return {
            Color.BLACK: [
                (1, 1), (2, 2)
            ],
            Color.WHITE: [
                (2, 1), (1, 2)
            ]
        }

    @staticmethod
    def ko_position():
        return {
            Color.BLACK: [
                (0, 1), (1, 0), (2, 1), (1, 2)
            ],
            Color.WHITE: [
                (0, 2), (2, 2), (1, 3)
            ]
        }
