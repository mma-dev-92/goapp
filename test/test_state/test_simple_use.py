from gologic.board.boardposition import BoardPosition
from gologic.board.color import Color
from gologic.state.state import State, initial_state
from test.utils.base import BaseTestCaseClass
import random


class TestSimpleUse(BaseTestCaseClass):
    def test_init_invalid_type_board_position_argument(self):
        self.__test_init_raises_with_args(
            TypeError,
            prev_pos='something something dark side',
            now_pos=13
        )

    def test_init_different_sizes_board_position_argument(self):
        self.__test_init_raises_with_args(
            RuntimeError,
            prev_pos=BoardPosition(size=9),
            now_pos=BoardPosition(size=13)
        )

    def test_init_invalid_keys_type_captured_argument(self):
        self.__test_init_raises_with_args(
            KeyError,
            captured={
                'BLACK': 10,
                Color.WHITE: 3
            }
        )

    def test_init_invalid_values_type_captured_argument(self):
        self.__test_init_raises_with_args(
            TypeError,
            captured={
                Color.BLACK: '10',
                Color.WHITE: 3
            }
        )

    def test_init_negative_values_captured_argument(self):
        self.__test_init_raises_with_args(
            ValueError,
            captured={
                Color.BLACK: 100,
                Color.WHITE: -30
            }
        )

    def test_init_invalid_to_move_argument(self):
        self.__test_init_raises_with_args(
            TypeError,
            to_move='WHITE'
        )

    def __test_init_raises_with_args(self, exception, prev_pos=None, now_pos=None, captured=None, to_move=None):
        if not prev_pos or not now_pos:
            random_size = self.random_size()
            prev_pos = self.fill(BoardPosition(random_size), self.random_coordinates(random_size))
            now_pos = self.fill(BoardPosition(random_size), self.random_coordinates(random_size))
        if not captured:
            captured = {
                Color.BLACK: random.randint(0, 100),
                Color.WHITE: random.randint(0, 100)
            }
        if not to_move:
            to_move = self.random_color()
        with self.assertRaises(exception):
            State(prev_pos, now_pos, captured, to_move)
