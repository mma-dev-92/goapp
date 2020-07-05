from gologic.state.state import initial_state
from gologic.board.color import Color
from test.utils.base import BaseTestCaseClass


class TestInitialState(BaseTestCaseClass):
    def setUp(self):
        super(TestInitialState, self).setUp()
        self.rand_size = self.random_size()
        self.init_state = initial_state(self.rand_size)

    def test_initial_state_zero_captured(self):
        self.assertTrue(self.init_state.captured_white_stones == 0 and self.init_state.captured_black_stones == 0)

    def test_initial_state_to_move_color_is_black(self):
        self.assertEqual(self.init_state.to_move, Color.BLACK)

    def test_initial_state_now_position_is_initial(self):
        self.assertTrue(self.init_state.now_position.initial())

    def test_initial_state_prev_position_is_initial(self):
        self.assertTrue(self.init_state.prev_position.initial())
