from gologic.state.state import initial_state
from test.utils.base import BaseTestCaseClass


class TestInitialState(BaseTestCaseClass):
    def test_initial_state_zero_captured(self):
        init_state = initial_state()
        self.assertTrue(init_state.captured_black_stones == 0 and init_state.captured_white_stones == 0)

    def test_initial_state_prev_position_is_none(self):
        self.assertIsNone(initial_state().prev_position)

    def test_initial_state_now_position_all_fields_empty(self):
        pass

    def test_initial_state_to_move_color_is_black(self):
        pass
