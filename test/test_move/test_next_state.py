from test.utils.base import BaseTestCaseClass
from gologic.state.state import State
from gologic.move.move import next_state
from gologic.board.boardposition import BoardPosition


class TestNextState(BaseTestCaseClass):
    """
    Here I am just testing if the violation of a ko rule is correct, and if capturing the stones works correctly.
    All other rules are taken care of in the move.next_position function.
    """

    def test_random_move_from_initial_state(self):
        random_size = self.random_size()
        init_state = State.initial_state(size=random_size)
        random_coordinates = self.random_coord(size=random_size)
        random_color = self.random_color()

        next_state_result = next_state(state=init_state, coordinates=random_coordinates, color=random_color)
        next_state_expected = State(
            prev_pos=BoardPosition(size=random_size),
            now_pos=BoardPosition(size=random_size).set_field(random_coordinates, random_color)
        )

        self.assertTrue(next_state_result == next_state_expected)

    def test_capture_one_stone(self):
        pass

    def capture_several_stones(self):
        pass

    def test_violation_of_ko_rule_raises_illegal_position_error(self):
        pass

    def test_ko_played_correctly(self):
        pass
