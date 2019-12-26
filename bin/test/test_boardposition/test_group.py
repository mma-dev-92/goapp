import unittest
from itertools import product
from pprint import pprint

from .base import BaseTestCaseClass
from ...gologic.board.boardposition import BoardPosition
from ...gologic.board.field import Field, EmptyField, NonEmptyField, Color


class TestGroup(BaseTestCaseClass):
    def test_empty_group(self):
        empty = self.random_size_empty_board()
        self.assertEqual(empty.group(self.random_coord(size=empty.size)), [])

    def test_diagonal_stones_one_color(self):
        self.__do_test(groups={
            Color.BLACK: [
                [(0, 0)], [(0, 2)], [(2, 0)], [(1, 1)]
            ]
        })

    def test_diagonal_stones_both_color(self):
        self.__do_test(groups={
            Color.BLACK: [
                [(1, 1)], [(2, 2)]
            ],
            Color.WHITE: [
                [(2, 1)], [(1, 2)]
            ]
        })

    def test_max_size_group(self):
        random_size = self.random_size()
        max_size_group = list(product(range(random_size), range(random_size)))
        max_size_group.remove(self.random_coord(size=random_size))
        self.__do_test(groups={
            Color.BLACK: [max_size_group]
        }, size=random_size)

    def test_simple_board_position(self):
        self.__do_test(groups={
            Color.BLACK: [
                [(0, 2), (1, 2), (1, 1)],
                [(2, 0)],
                [(1, 4), (2, 4), (3, 4), (2, 3), (2, 5)]
            ],
            Color.WHITE: [
                [(0, 1)],
                [(1, 0)],
                [(2, 1), (2, 2), (3, 1), (3, 2), (3, 3)]
            ]
        })

    def __do_test(self, groups, size=None):
        size = size if size else self.random_size()
        bp = self.empty_board(size=size)
        for color, coords in groups.items():
            for group_coords in coords:
                bp = self.fill(bp, {color: group_coords})
        result = {color: self.__get_groups(bp, coords) for color, coords in groups.items()}
        expected_result = groups
        self.assertTrue(self.__deep_compare(groups, result))

    def __deep_compare(self, d1, d2):
        for k1 in d1:
            if k1 not in d2:
                return False
            if not self.__compare_lists(d1[k1], d2[k1]):
                return False
        return True

    def __compare_lists(self, l1, l2):
        for e1, e2 in zip(l1, l2):
            if not sorted(e1) == sorted(e2):
                return False
        return True

    def __get_groups(self, bp, coords):
        return [bp.group(group_coords[0]) for group_coords in coords]
