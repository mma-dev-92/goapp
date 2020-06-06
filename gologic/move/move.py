from gologic.board.boardposition import BoardPosition
from gologic.state.state import State


class IllegalMoveError(Exception):
    pass


class SuicideMoveError(IllegalMoveError):
    pass


class OccupiedFieldMoveError(IllegalMoveError):
    pass


class RepeatedPositionMoveError(IllegalMoveError):
    pass


def next_state(state, coordinates, color):
    pass


def next_position(bp, coordinates, color):
    pass
