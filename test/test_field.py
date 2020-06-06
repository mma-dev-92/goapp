from gologic.board.field import Field, EmptyField, NonEmptyField, Color
from test.test_boardposition.base import BaseTestCaseClass


class TestField(BaseTestCaseClass):
    def test_abstract_class(self):
        self.__test_if_class_is_abstract(Field)

    def test_init_black_field(self):
        self.do_test_for_no_exception_rising(NonEmptyField, color=Color.BLACK)

    def test__init__white_field(self):
        self.do_test_for_no_exception_rising(NonEmptyField, color=Color.WHITE)

    def test__init__empty_field(self):
        self.do_test_for_no_exception_rising(EmptyField)

    def test_eq_two_black_fields(self):
        self.assertEqual(self.__black_field(), self.__black_field())

    def test_eq_two_white_fields(self):
        self.assertEqual(self.__white_field(), self.__white_field())

    def test_eq_two_empty_fields(self):
        self.assertEqual(EmptyField(), EmptyField())

    def test_empty_not_equal_nonempty(self):
        self.assertNotEqual(EmptyField(), self.__white_field())

    def test_field_not_equal_none(self):
        with self.assertRaises(TypeError):
            EmptyField().__eq__(None)

    def test_field_not_equal_string(self):
        with self.assertRaises(TypeError):
            NonEmptyField(Color.BLACK) == 'field'

    def test_is_empty_on_nonempty(self):
        self.assertFalse(self.__black_field().is_empty())

    def test_is_empty_on_empty(self):
        self.assertTrue(EmptyField().is_empty())

    def test_is_black_on_black(self):
        self.assertTrue(self.__black_field().is_black())

    def is_black_on_white(self):
        self.assertFalse(self.__white_field().is_black())

    def test_is_black_on_empty(self):
        self.assertFalse(EmptyField().is_black())

    def test_is_white_on_white(self):
        self.assertTrue(self.__white_field().is_white())

    def test_is_white_on_black(self):
        self.assertFalse(self.__black_field().is_white())

    def test_is_white_on_empty(self):
        self.assertFalse(self.__black_field().is_white())

    def test_color_black_field(self):
        self.assertTrue(self.__black_field().color == Color.BLACK)

    def test_color_white_field(self):
        self.assertTrue(self.__white_field().color == Color.WHITE)

    def test_color_enpty_field(self):
        self.assertIsNone(EmptyField().color)

    def test_nonempty_field_color_immutable(self):
        with self.assertRaises(AttributeError):
            self.__black_field().color = Color.BLACK

    def test_empty_field_color_immutable(self):
        with self.assertRaises(AttributeError):
            EmptyField().color = Color.WHITE

    @staticmethod
    def __black_field():
        return NonEmptyField(color=Color.BLACK)

    @staticmethod
    def __white_field():
        return NonEmptyField(color=Color.WHITE)

    def __test_if_class_is_abstract(self, to_test):
        with self.assertRaises(TypeError):
            to_test()
