from itertools import product

from test.utils.base import BaseTestCaseClass
from gologic.board.color import Color


class TestLiberties(BaseTestCaseClass):

    def test_random_coord_on_empty_board(self):
        bp = self.random_size_empty_board()
        random_coord = self.random_coord(bp.size)
        with self.assertRaises(RuntimeError, msg=self.error_msg(bp, random_coord, None, RuntimeError)):
            bp.liberties(random_coord)

    def test_single_stone_on_the_middle(self):
        self.__do_the_test(
            coord=(3, 3),
            coordinates={
                Color.BLACK: [(3, 3)]
            },
            expected_result=4
        )

    def test_single_stone_in_the_corner(self):
        self.__do_the_test(
            coord=(0, 0),
            coordinates={
                Color.WHITE: [(0, 0)]
            },
            expected_result=2
        )

    def test_single_stone_on_side(self):
        self.__do_the_test(
            coord=(1, 0),
            coordinates={
                Color.WHITE: [(1, 0)]
            },
            expected_result=3
        )

    def test_5_group_stones_only(self):
        self.__do_the_test(
            coord=(2, 2),
            coordinates={
                Color.BLACK: [(2, 0), (2, 1), (2, 2), (3, 1), (1, 1)]
            },
            expected_result=7
        )

    def test_two_colors_on_board1(self):
        self.__do_test_with_two_colors(coord=(1, 1), expected_result=2)

    def test_two_colors_on_board2(self):
        self.__do_test_with_two_colors(coord=(0, 1), expected_result=1)

    def test_two_colors_on_board3(self):
        self.__do_test_with_two_colors(coord=(0, 1), expected_result=1)

    def test_two_colors_on_board4(self):
        self.__do_test_with_two_colors(coord=(2, 0), expected_result=1)

    def test_two_colors_on_board5(self):
        self.__do_test_with_two_colors(coord=(2, 3), expected_result=6)

    def test_two_colors_on_board6(self):
        self.__do_test_with_two_colors(coord=(2, 2), expected_result=4)

    def test_all_but_one_fields_in_one_color(self):
        size = self.random_size()
        coordinates = list(product(range(size), range(size)))
        coordinates.remove((size - 1, size - 1))
        self.__do_the_test(
            coord=(0, 0),
            coordinates={
                Color.BLACK: coordinates
            },
            expected_result=1,
            size=size
        )

    def __do_test_with_two_colors(self, coord, expected_result):
        self.__do_the_test(
            coord=coord,
            coordinates=self.two_colors_coordinates(),
            expected_result=expected_result
        )

    def __do_the_test(self, coord, coordinates, expected_result, size=None):
        size = size if size else self.random_size()
        bp = self.empty_board(size)
        bp = self.fill(bp, coordinates)
        result = bp.liberties(coord)
        self.assertEqual(result, expected_result,
                         msg=self.error_msg(bp, coord, result, expected_result))
