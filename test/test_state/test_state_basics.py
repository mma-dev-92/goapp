import random

from test.utils.base import BaseTestCaseClass
from gologic.state.state import State


class TestStateBasics(BaseTestCaseClass):
    def test_position(self):
        random_size = self.random_size()
        random_pos_1, random_pos_2 = (
            self.fill(self.empty_board(random_size), self.random_coordinates(random_size)),
            self.fill(self.empty_board(random_size), self.random_coordinates(random_size)),
        )

        state = State(random_pos_1, random_pos_2)

        self.assertTrue(state.prev_position == random_pos_1 and state.position == random_pos_2)

    def test_position_different_sizes_raises_type_error(self):
        with self.assertRaises(TypeError):
            size_1, size_2 = self.two_random_sizes()
            State(
                self.fill(self.empty_board(size_1), self.random_coordinates(size_1)),
                self.fill(self.empty_board(size_2), self.random_coordinates(size_2)),
            )

    def test_non_empty_prev_position_and_empty_position_raises_type_error(self):
        with self.assertRaises(TypeError):
            rand_size = self.random_size()
            State(
                self.fill(self.empty_board(rand_size), self.random_coordinates(rand_size)),
                self.empty_board(rand_size),
            )

    def test_captured_stones_default_arg(self):
        random_size = self.random_size()
        state = State(self.empty_board(random_size), self.empty_board(random_size))

        self.assertTrue(state.captured_black_stones == 0 and state.captured_white_stones == 0)

    def test_captured_stones_given_arg(self):
        random_size = self.random_size()
        rand_black_captured = random.randint(0, random_size ** 2)
        rand_white_captured = random.randint(0, random_size ** 2)

        state = State(
            self.empty_board(random_size), self.empty_board(random_size),
            b_captured=rand_black_captured, w_captured=rand_white_captured
        )

        self.assertTrue(
            state.captured_black_stones == rand_black_captured and state.captured_white_stones == rand_white_captured)

    def test_negative_black_captured_stones_raises_value_error(self):
        rand_size = self.random_size()

        with self.assertRaises(ValueError):
            State(self.empty_board(rand_size), self.empty_board(rand_size), b_captured=3, w_captured=-4)

    def test_negative_white_captured_stones_raises_value_error(self):
        rand_size = self.random_size()

        with self.assertRaises(ValueError):
            State(self.empty_board(rand_size), self.empty_board(rand_size), b_captured=-234, w_captured=4)
