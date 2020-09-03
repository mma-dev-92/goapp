from test.utils.base import BaseTestCaseClass
from gologic.board.boardposition import BoardPosition
from gologic.board.field import Color


class TestBoardPositionSimpleUse(BaseTestCaseClass):
    def test__init__with_proper_size_value(self):
        self.do_test_for_no_exception_rising(BoardPosition, size=self.random_size())

    def test__init__with_string_size_value(self):
        with self.assertRaises(TypeError):
            BoardPosition("mama")

    def test__init__with_iterable_value(self):
        with self.assertRaises(TypeError):
            BoardPosition([19])

    def test__init__with_invalid_positive_int_value(self):
        with self.assertRaises(ValueError):
            BoardPosition(17)

    def test__init__with_invalid_negative_int_value(self):
        with self.assertRaises(ValueError):
            BoardPosition(-3)

    def test_size_for_immutability(self):
        with self.assertRaises(AttributeError):
            self.random_nonempty_board().size = 13

    def test_clear(self):
        bp = self.random_nonempty_board()
        bp.clear()
        self.assertEqual(bp, self.empty_board(bp.size))

    def test_empty(self):
        bp = BoardPosition(self.random_size())
        self.assertTrue(bp.empty)

    def test_after_initialization_board_is_empty(self):
        size = self.random_size()
        empty_board = self.empty_board(size)
        non_empty = list(filter(lambda f: not f.is_empty(),
                                [empty_board.at(c) for c in self.coordinates[size]]))
        self.assertTrue(len(non_empty) == 0)

    def test_set_field_on_empty_board(self):
        bp = self.random_size_empty_board()
        bp.set_field((1, 1), Color.BLACK)
        self.assertEqual(bp.at((1, 1)).color, Color.BLACK)

    def test_set_field_on_non_empty_board(self):
        bp = self.random_nonempty_board()
        bp.set_field((3, 4), Color.WHITE)
        self.assertEqual(bp.at((3, 4)).color, Color.WHITE)

    def test_clear_empty_field(self):
        bp = self.random_size_empty_board()
        random_coord = self.random_coord(bp.size)
        bp.clear_field(random_coord)
        self.assertTrue(bp.at(random_coord).is_empty())

    def test_clear_non_empty_field(self):
        bp = self.random_size_empty_board()
        random_coord = self.random_coord(bp.size)
        bp.set_field(random_coord, Color.BLACK)
        bp.clear_field(random_coord)
        self.assertTrue(bp.at(random_coord).is_empty())

    def test_index_out_of_range_boundary_values(self):
        bp = self.random_size_empty_board()
        with self.assertRaises(IndexError, msg="To big row value, exception not thrown"):
            bp.at((bp.size, 1))
        with self.assertRaises(IndexError, msg="To big column value, exception not thrown"):
            bp.at((1, bp.size))

    def test_index_out_of_range_negative_values(self):
        bp = self.random_size_empty_board()
        with self.assertRaises(IndexError, msg="Negative column value, exception not thrown"):
            bp.at((-1, 1))
        with self.assertRaises(IndexError, msg="Negative column value, exception not thrown"):
            bp.at((1, -1))

    def test_wrong_index_type(self):
        bp = self.random_size_empty_board()
        for index in ['2', 3.45, "mama", [1, 2, 3], [1, 2]]:
            with self.assertRaises(TypeError, msg="index type {}, exception not thrown".format(type(index))):
                bp.at(index)

    def test__eq__different_sizes(self):
        random_size = self.random_size()
        bp = self.empty_board(random_size)
        other = self.empty_board(self.other_sizes(random_size)[0])
        with self.assertRaises(ValueError):
            bp.__eq__(other)

    def test__eq__wrong_other_object_type(self):
        bp = self.random_size_empty_board()
        for other in [23, "other!"]:
            with self.assertRaises(TypeError, msg="__eq__: other object of type: {}, exception not thronw".format(type(other))):
                bp.__eq__(other)

    def test__eq__empty_objects(self):
        random_size = self.random_size()
        self.assertTrue(self.empty_board(random_size), self.empty_board(random_size))

    def test__eq__when_nonempty_objects_are_equal(self):
        random_size = self.random_size()
        random_coords = self.random_coordinates(random_size, black=30, white=29)
        bp = self.fill(self.empty_board(random_size), random_coords)
        other = self.fill(self.empty_board(random_size), random_coords)
        self.assertTrue(bp == other)
