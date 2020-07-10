from gologic.board.boardposition import InitialBoardPosition, AbcBoardPosition
from gologic.board.color import Color
from typing import Dict
from copy import deepcopy


class State:
    def __init__(self, prev_pos: AbcBoardPosition, now_pos: AbcBoardPosition, captured: Dict[Color, int], to_move: Color):
        self.__check_board_positions(prev_pos, now_pos)
        self.__prev_position, self.__now_position = prev_pos, now_pos
        self.__check_captured(captured)
        self.__captured = captured
        self.__check_to_move(to_move)
        self.__to_move = to_move

    @property
    def prev_position(self):
        return deepcopy(self.__prev_position)

    @property
    def now_position(self):
        return deepcopy(self.__now_position)

    @property
    def captured_black_stones(self):
        return self.__captured[Color.BLACK]

    @property
    def captured_white_stones(self):
        return self.__captured[Color.WHITE]

    @property
    def to_move(self):
        return self.__to_move

    @staticmethod
    def __check_captured(captured):
        if not isinstance(captured, dict):
            raise TypeError("captured must be a dictionary")
        if not set(captured.keys()) == {Color.BLACK, Color.WHITE}:
            raise KeyError("captured has to have only two keys: Color.BLACK and Color.WHITE")
        if not isinstance(captured[Color.BLACK], int) or not isinstance(captured[Color.WHITE], int):
            raise TypeError("values of captured have to be ints")
        if captured[Color.BLACK] < 0 or captured[Color.WHITE] < 0:
            raise ValueError("values of captured have to be non negative")

    @staticmethod
    def __check_to_move(to_move):
        if not isinstance(to_move, Color):
            raise TypeError("to move have to be an instance of gologic.board.color.Color class")

    @staticmethod
    def __check_board_positions(prev_pos, now_pos):
        if not isinstance(prev_pos, AbcBoardPosition) or not isinstance(now_pos, AbcBoardPosition):
            raise TypeError("gologic.board.color.AbcBoardPosition type required")
        if not prev_pos.size == now_pos.size:
            raise RuntimeError("prev_pos and now_pos have different size!")
        if not prev_pos.initial() and now_pos.initial():
            raise RuntimeError("now position is initial, but prev position is not!")

    def next_state(self, coordinates, color):
        pass


def initial_state(size: int) -> State:
    return State(
        prev_pos=InitialBoardPosition(size),
        now_pos=InitialBoardPosition(size),
        captured={
            Color.BLACK: 0,
            Color.WHITE: 0
        },
        to_move=Color.BLACK
    )
