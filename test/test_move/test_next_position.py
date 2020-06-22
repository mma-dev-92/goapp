import random

from test.utils.base import BaseTestCaseClass
from gologic.move.move import next_position, OccupiedFieldMoveError, SuicideMoveError
from gologic.board.boardposition import BoardPosition
from gologic.board.color import Color


class TestNextPosition(BaseTestCaseClass):

    def test_suicide_move_u_like_shape(self):
        bp = self.fill(BoardPosition(self.random_size()), self.u_like_position())
        color = Color.BLACK
        coordinate = (1, 0)
        with self.assertRaises(SuicideMoveError, msg=self.error_msg(bp, (coordinate, color), None, SuicideMoveError)):
            next_position(bp, coordinate, color)

    def test_capture_u_like_shape(self):
        self.__do_the_test(
            input_board_conf=self.u_like_position(),
            expected_board_conf=self.alter_board_conf(
                conf=self.u_like_position(),
                to_add={Color.WHITE: [(1, 0)]},
                to_remove={Color.BLACK: [(0, 0), (0, 1), (1, 1), (2, 1), (2, 0)]},
            ),
            color=Color.WHITE,
            move_cord=(1, 0)
        )

    def test_ko(self):
        self.__do_the_test(
            input_board_conf=self.ko_position(),
            expected_board_conf=self.alter_board_conf(
                conf=self.ko_position(),
                to_remove={Color.BLACK: [(1, 2)]},
                to_add={Color.WHITE: [(1, 1)]}
            ),
            color=Color.WHITE,
            move_cord=(1, 1)
        )

    def test_suicide_move_error(self):
        size = self.random_size()
        bp = self.fill(BoardPosition(size), self.diagonal_stones_one_color_position())
        coordinate, color = (1, 0), Color.WHITE
        with self.assertRaises(SuicideMoveError, msg=self.error_msg(bp, (coordinate, color), None, SuicideMoveError)):
            next_position(bp, coordinate, color)

    def test_move_on_empty_board(self):
        size = self.random_size()
        color = Color.BLACK
        move_cord = self.random_coord(size)
        self.__do_the_test(
            input_board_conf={},
            expected_board_conf={color: [move_cord]},
            color=color,
            move_cord=move_cord,
            size=size
        )

    def test_occupied_field_move_error(self):
        board_conf = self.two_colors_coordinates()
        in_data = random.choice(board_conf[self.random_color()]), self.random_color()
        bp = self.fill(BoardPosition(self.random_size()), board_conf)
        with self.assertRaises(OccupiedFieldMoveError, msg=self.error_msg(bp, in_data, None, OccupiedFieldMoveError)):
            next_position(bp, *in_data)

    def test_capture_with_quasi_suicide_move1(self):
        self.__do_the_test(
            input_board_conf=self.two_colors_coordinates(),
            expected_board_conf=self.alter_board_conf(
                conf=self.two_colors_coordinates(),
                to_remove={Color.WHITE: [(0, 1), (1, 0)]},
                to_add={Color.BLACK: [(0, 0)]}
            ),
            color=Color.BLACK,
            move_cord=(0, 0)
        )

    def test_capture_with_quasi_suicide_move2(self):
        self.__do_the_test(
            input_board_conf=self.alter_board_conf(
                conf=self.two_colors_coordinates(),
                to_remove={},
                to_add={Color.WHITE: [(0, 4)], Color.BLACK: [(0, 3)]},
            ),
            expected_board_conf=self.alter_board_conf(
                conf=self.two_colors_coordinates(),
                to_remove={Color.BLACK: [(0, 2), (1, 1), (1, 2)]},
                to_add={Color.WHITE: [(0, 4), (1, 3)]}
            ),
            color=Color.WHITE,
            move_cord=(1, 3)
        )

    def __do_the_test(self, input_board_conf, expected_board_conf, color, move_cord, size=None):
        size = size if size else self.random_size()
        input_position = self.fill(BoardPosition(size), input_board_conf)
        expected_result = self.fill(BoardPosition(size), expected_board_conf)
        result = next_position(input_position, color, move_cord)
        self.assertEqual(result, expected_result, msg=self.error_msg(
            bp=input_position,
            input_data=(move_cord, color),
            expected_result=self.print_position(expected_result),
            result=self.print_position(result))
        )
