from gologic.board.field import Color
from test.utils.base import BaseTestCaseClass


class TestColor(BaseTestCaseClass):
    def test__eq__1(self):
        rand_color = self.random_color()
        self.assertTrue(rand_color == rand_color)

    def test__eq__2(self):
        rand_color = self.random_color()
        self.assertFalse(rand_color == rand_color.opposite())

    def test__eq__3(self):
        self.assertFalse(Color.WHITE == Color.BLACK)
