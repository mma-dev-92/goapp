from itertools import product
import random

from test.utils.base import BaseTestCaseClass
from gologic.board.field import Color


class TestGroup(BaseTestCaseClass):

    def test_empty_group(self):
        empty = self.random_size_empty_board()
        self.assertEqual(empty.group(self.random_coord(size=empty.size)), [])

    def test_diagonal_stones_one_color1(self):
        self.__diagonal_stones_one_color_test(group=[(0, 0)])

    def test_diagonal_stones_one_color2(self):
        self.__diagonal_stones_one_color_test(group=[(0, 2)])

    def test_diagonal_stones_one_color3(self):
        self.__diagonal_stones_one_color_test(group=[(1, 1)])

    def test_diagonal_stones_one_color4(self):
        self.__diagonal_stones_one_color_test(group=[(2, 0)])

    def __diagonal_stones_one_color_test(self, group):
        self.__do_the_test(coordinates=self.diagonal_stones_one_color_position(), group=group)

    def test_diagonal_stones_both_color1(self):
        self.__diagonal_stones_both_color_test(group=[(1, 1)])

    def test_diagonal_stones_both_color2(self):
        self.__diagonal_stones_both_color_test(group=[(2, 2)])

    def test_diagonal_stones_both_color3(self):
        self.__diagonal_stones_both_color_test(group=[(1, 2)])

    def test_diagonal_stones_both_color4(self):
        self.__diagonal_stones_both_color_test(group=[(2, 1)])

    def __diagonal_stones_both_color_test(self, group):
        self.__do_the_test(coordinates=self.diagonal_stones_both_color_position(), group=group)

    def test_max_size_group(self):
        random_size = self.random_size()
        coordinates = self.__max_size_group(random_size)
        self.__do_the_test(coordinates=coordinates, group=coordinates[Color.BLACK], size=random_size)

    def test_simple_board_position1(self):
        self.__simple_board_position_test(group=[(6, 2), (7, 2), (6, 1)])

    def test_simple_board_position2(self):
        self.__simple_board_position_test(group=[(2, 0)])

    def test_simple_board_position3(self):
        self.__simple_board_position_test(group=[(1, 4), (2, 4), (3, 4), (2, 3), (2, 5)])

    def test_simple_board_position4(self):
        self.__simple_board_position_test(group=[(0, 1)])

    def test_simple_board_position5(self):
        self.__simple_board_position_test(group=[(1, 0)])

    def test_simple_board_position6(self):
        self.__simple_board_position_test(group=[(2, 1), (2, 2), (3, 1), (3, 2), (3, 3)])

    def __simple_board_position_test(self, group):
        self.__do_the_test(coordinates=self.simple_board_position(), group=group)

    def __max_size_group(self, size):
        return {
            Color.BLACK: self.__all_but_one_fields(size)
        }

    def __all_but_one_fields(self, size):
        coord_to_rmv = self.random_coord(size)
        return [x for x in list(product(range(size), range(size))) if not x == coord_to_rmv]

    def __do_the_test(self, coordinates, group, size=None):
        size = size if size else self.random_size()
        bp = self.fill(self.empty_board(size), coordinates)
        input_data = random.choice(group)
        result = sorted(bp.group(input_data))
        expected_result = sorted(group)
        self.assertEqual(result, expected_result, msg=self.error_msg(bp, input_data, result, expected_result))
