from test.utils.base import BaseTestCaseClass


class TestNextState(BaseTestCaseClass):
    """
    Here I am just testing if the violation of a ko rule is correct, and if capturing the stones works correctly.

    All other rules are taken care of in the move.next_position function.
    """

    def test_random_move_from_initial_state(self):
        pass

    def test_capture_one_stone(self):
        pass

    def capture_several_stones(self):
        pass

    def test_violation_of_ko_rule_raises_illegal_position_error(self):
        pass

    def test_ko_played_correctly(self):
        pass
