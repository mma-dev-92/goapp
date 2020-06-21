from gologic.board.boardposition import BoardPosition
from typing import Tuple
from gologic.state.state import State
from gologic.board.color import Color


class IllegalMoveError(Exception):
    pass


class SuicideMoveError(IllegalMoveError):
    pass


class OccupiedFieldMoveError(IllegalMoveError):
    pass


class IllegalPositionError(Exception):
    pass


class RepeatedPositionMoveError(IllegalPositionError):
    pass


def next_state(state: State, coordinates: Tuple[int, int], color: Color):
    pass


def next_position(bp: BoardPosition, coordinates: Tuple[int, int], color: Color):
    return bp
