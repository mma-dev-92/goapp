from random import choice

from .base import BaseTestCaseClass
from ...gologic.board.boardposition import BoardPosition


class TestNeighbours(BaseTestCaseClass):
    def test_corner(self):
        self.__do_the_test(coord=(0, 0), expected_result=[(0, 1), (1, 0)])

    def test_edge(self):
        self.__do_the_test(coord=(2, 0), expected_result=[(1, 0), (3, 0), (2, 1)])

    def test_middle(self):
        self.__do_the_test(coord=(3, 2), expected_result=[(3, 1), (3, 3), (2, 2), (4, 2)])

    def test_edge_with_size_value_indexes(self):
        bp = self.random_nonempty_board()
        self.__do_the_test_with_specyfic_bp(
            (bp.size-1, bp.size-1), [(bp.size-2, bp.size-1), (bp.size-1, bp.size-2)], bp)

    def __do_the_test(self, coord, expected_result):
        board = self.random_size_empty_board()
        result = board.neighbours(coord)
        self.assertEqual(sorted(result), sorted(expected_result))

    def __do_the_test_with_specyfic_bp(self, coord, expected_result, bp):
        result = bp.neighbours(coord)
        self.assertEqual(sorted(result), sorted(expected_result))
