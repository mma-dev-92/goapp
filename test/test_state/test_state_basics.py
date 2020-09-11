import random

from test.utils.base import BaseTestCaseClass
from gologic.state.state import State
from gologic.board.boardposition import BoardPosition


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

    def test_initial_state_emptiness(self):
        init_state = State.initial_state(size=self.random_size())

        self.assertTrue(init_state.prev_position == init_state.position and init_state.prev_position.empty)

    def test_initial_state_captured_stones(self):
        init_state = State.initial_state(size=self.random_size())

        self.assertTrue(init_state.captured_black_stones == 0 and init_state.captured_white_stones == 0)

    def test__eq__(self):
        empty_pos, rand_pos = self.__random_same_size_positions()
        self.assertTrue(State(empty_pos, rand_pos) == State(empty_pos, rand_pos))

    def test__eq__different_captured_black(self):
        empty_pos, rand_pos = self.__random_same_size_positions()
        self.assertFalse(State(empty_pos, rand_pos, b_captured=4) == State(empty_pos, rand_pos, b_captured=8))

    def test__eq__different_captured_white(self):
        empty_pos, rand_pos = self.__random_same_size_positions()
        self.assertFalse(State(empty_pos, rand_pos, w_captured=4) == State(empty_pos, rand_pos, w_captured=11))

    def test__eq__different_prev_pos(self):
        empty_pos, rand_pos = self.__random_same_size_positions()
        self.assertFalse(
            State(empty_pos, rand_pos) == State(self.random_nonempty_board(size=rand_pos.size), rand_pos)
        )

    def test__eq__different_now_pos(self):
        empty_pos, rand_pos = self.__random_same_size_positions()
        self.assertFalse(
            State(empty_pos, rand_pos) == State(empty_pos, self.random_nonempty_board(size=rand_pos.size))
        )

    def __random_same_size_positions(self):
        random_pos = self.random_nonempty_board()
        empty_pos = BoardPosition(size=random_pos.size)

        return empty_pos, random_pos
