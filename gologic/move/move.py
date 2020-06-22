from copy import deepcopy

from gologic.board.boardposition import BoardPosition
from gologic.board.field import EmptyField
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
    # if the target field is not empty - error
    if not bp.at(coordinates).is_empty():
        raise OccupiedFieldMoveError

    # make a deepcopy.copy of bp and place there given stone
    bp_copy = deepcopy(bp)
    bp_copy.set_field(coordinates, color)

    # check if placed stone kills something
    for neighbor_coordinate in bp_copy.neighbors(coordinates):
        if not bp_copy.at(neighbor_coordinate).is_empty() and bp_copy.at(neighbor_coordinate).color == color.opposite():
            bp_copy = __kill_group_if_zero_liberties(bp_copy, neighbor_coordinate)

    # check if the placed stone has > 0 liberties
    if bp_copy.liberties(coordinates) == 0:
        raise SuicideMoveError

    return bp_copy


def __kill_group_if_zero_liberties(bp: BoardPosition, coordinate: Tuple[int, int]):
    if not bp.liberties(coordinate) == 0:
        return bp
    for group_member_coordinates in bp.group(coordinate):
        bp.clear_field(group_member_coordinates)
    return bp
