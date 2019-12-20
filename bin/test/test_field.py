import unittest

from ..gologic.board.field import Field, EmptyField, NonEmptyField, Color
from .test_boardposition.base import BaseTestCaseClass


class TestField(BaseTestCaseClass):
    def test_abstract_class(self):
        self.__test_if_class_is_abstract(Field)

    def test_init_black_field(self):
        self.do_test_for_no_exception_rising(NonEmptyField, color=Color.BLACK)

    def test__init__white_field(self):
        self.do_test_for_no_exception_rising(NonEmptyField, color=Color.WHITE)

    def test__init__empty_field(self):
        self.do_test_for_no_exception_rising(EmptyField)

    def test_eq(self):
        non_empty_black_1 = NonEmptyField(color=Color.BLACK)
        non_empty_black_2 = NonEmptyField(color=Color.BLACK)
        non_empty_white_1 = NonEmptyField(color=Color.WHITE)
        non_empty_white_2 = NonEmptyField(color=Color.WHITE)

        self.assertTrue(non_empty_black_1 == non_empty_black_2)
        self.assertTrue(non_empty_white_1 == non_empty_white_2)

        self.assertFalse(non_empty_white_1 == non_empty_black_2)

        empty = EmptyField()

        with self.assertRaises(ValueError):
            empty == non_empty_black_2

        for value in [1, 'maciek', {1: 1}]:
            with self.assertRaises(TypeError):
                empty == value

    def test_is_empty(self):
        non_empty_black = NonEmptyField(color=Color.BLACK)
        non_empty_white = NonEmptyField(color=Color.WHITE)
        empty = EmptyField()

        self.assertTrue(empty.is_empty())
        self.assertFalse(non_empty_black.is_empty())
        self.assertFalse(non_empty_white.is_empty())

    def __test_if_class_is_abstract(self, to_test):
        with self.assertRaises(TypeError):
            to_test()
