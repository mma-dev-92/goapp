import unittest
from itertools import product

from .base_test_case import BaseTestCase
from ...gologic.board.boardposition import BoardPosition
from ...gologic.board.field import Field, EmptyField, NonEmptyField, Color


class TestGroup(BaseTestCase):
    def setUp(self):
        super().setUp()

    def test_empty_group(self):
        for size in self.valid_sizes:
            bp = Position(size)
            for coord in self.coords[size]:
                self.assertEqual(bp.group(coord), [])

    def test_diagonal_stones_one_color(self):
        for size in self.valid_sizes:
            bp = Position(size)
            coords = {
                Color.BLACK: [(0, 0), (0, 2), (2, 0), (1, 1)]
            }
            self.fill(bp, coords)
            for coord in black_single_groups:
                self.assertEqual(bp.group(coord), [coord])

    def test_diagonal_stones_both_color(self):
        for size in self.valid_sizes:
            bp = Position(size)
            coords = {
                Color.BLACK: [(1, 1), (2, 2)],
                Color.WHITE: [(2, 1), (1, 2)]
            }
            self.fill(bp, coords)
            for color in coords:
                for coord in coords[color]:
                    self.assertEqual(bp.group(coord), [coord])

    def test_max_size_group(self):
        for size in self.valid_sizes:
            bp = BoardPosition(size)
            coords = {
                Color.BLACK: self.coords[size]
            }
            excluded_fields = [
                (0, 0), (size - 1, size - 1), (0, 2), (2, 5), (3, 0)]
            for excluded_field in excluded_fields:
                self.fill(bp, coords)
                bp.set_field(excluded_field, Color.BLACK)
                for coord in expected_result:
                    self.assertEqual(bp.group(coord), expected_result)
                self.assertEqual(bp.group(excluded_field), [])

    def test_simple_board_position(self):
        for size in self.valid_sizes:
            bp = BoardPosition(size)
            black_groups = [
                [(0, 2), (1, 2), (1, 1)],
                [(2, 0)],
                [(1, 4), (2, 4), (3, 4), (2, 3), (2, 5)]
            ]
            white_groups = [
                [(0, 1)],
                [(1, 0)],
                [(2, 1), (2, 2), (3, 1), (3, 2), (3, 3)]
            ]
            coords = {
                Color.BLACK: [
                    x for group in black_groups for x in group],
                Color.WHITE: [
                    x for group in white_groups for x in group]
            }
            self.fill(bp, coords)
