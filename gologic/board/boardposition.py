from __future__ import annotations
from itertools import product
from abc import ABC, abstractmethod
from typing import Tuple
from copy import deepcopy

from gologic.board.field import EmptyField, NonEmptyField, Field
from gologic.board.color import Color


class IllegalMoveError(Exception):
    pass


class SuicideMoveError(IllegalMoveError):
    pass


class OccupiedFieldMoveError(IllegalMoveError):
    pass


class IllegalPositionError(Exception):
    pass


class AbcBoardPosition(ABC):
    VALID_SIZES = [9, 13, 19]

    def __init__(self, size: int):
        self.__check_size(size)
        self.__size = size

    @abstractmethod
    def initial(self) -> bool:
        pass

    @property
    def size(self):
        return self.__size

    def __eq__(self, other):
        if not isinstance(other, AbcBoardPosition):
            raise TypeError("can not compare AbcBoardPosition to {}".format(type(other)))
        if not self.initial() == other.initial():
            raise TypeError("can not compare initial and non initial board positions")
        if not self.size == other.size:
            raise RuntimeError("can not compare AbcBoardPosition of size {} with AbcBoardPosition of size {}".format(
                self.size, other.size))
        return True

    def __check_size(self, size):
        if not isinstance(size, int):
            raise TypeError("size must be an int")
        if size not in self.VALID_SIZES:
            raise ValueError("size must be one of {}".format(self.VALID_SIZES))

    @abstractmethod
    def next_position(self, coordinates: Tuple[int, int], color: Color):
        pass


class InitialBoardPosition(AbcBoardPosition):
    def __init__(self, size):
        super(InitialBoardPosition, self).__init__(size)
        
    def __eq__(self, other):
        return super(InitialBoardPosition, self).__eq__(other)

    def initial(self) -> bool:
        return True

    def next_position(self, coordinates: Tuple[int, int], color: Color):
        result = BoardPosition(self.size)
        result.set_field(coordinates, color)
        return result


class BoardPosition(AbcBoardPosition):
    def __init__(self, size):
        super(BoardPosition, self).__init__(size)
        self.__board_mask = {coord: EmptyField() for coord in product(range(size), range(size))}

    def initial(self) -> bool:
        return False

    @property
    def coordinates(self):
        return self.__board_mask.keys()

    def clear(self):
        for coord in self.__board_mask:
            self.__board_mask[coord] = EmptyField()

    def at(self, coord) -> Field:
        self.__check_coord(coord)
        return self.__board_mask[coord]

    def set_field(self, coord, color):
        self.__check_coord(coord)
        self.__board_mask[coord] = NonEmptyField(color)

    def clear_field(self, coord):
        self.__check_coord(coord)
        self.__board_mask[coord] = EmptyField()

    def __eq__(self, other):
        return super(BoardPosition, self).__eq__(other) and self.__board_mask == other.__board_mask

    def bind(self, operation, neutral_elem, start_coord, stop_before=lambda x: False, stop_after=lambda x: False):
        result = neutral_elem
        visited, to_visit = {coord: False for coord in self.coordinates}, {start_coord}
        while to_visit:
            v = to_visit.pop()
            if not stop_before(v):
                result = operation(result, v)
                if not stop_after(v):
                    to_visit.update([nv for nv in self.neighbors(v) if not visited[nv]])
            visited[v] = True
        return result

    def liberties(self, coord):
        if self.at(coord).is_empty():
            raise RuntimeError("trying to count liberties of an empty field")

        def f(val, _coord):
            return val + 1 if self.at(_coord).is_empty() else val

        def stop_before(_coord):
            return not self.at(_coord).is_empty() and not self.at(coord).color == self.at(_coord).color

        def stop_after(_coord):
            return self.at(_coord).is_empty()

        return self.bind(operation=f, neutral_elem=0, start_coord=coord, stop_before=stop_before, stop_after=stop_after)

    def group(self, coord):
        if self.at(coord).is_empty():
            return []

        def f(val, _coord):
            return val + [_coord] if self.at(_coord) == self.at(coord) else val

        def stop_before(_coord):
            return not self.at(_coord) == self.at(coord)

        return self.bind(operation=f, neutral_elem=[], start_coord=coord, stop_before=stop_before)

    def neighbors(self, coord):
        row, col = coord
        return [(row + row_transl, col) for row_transl in self.__get_transl(row)] + \
            [(row, col + col_transl) for col_transl in self.__get_transl(col)]

    def next_position(self, coordinates: Tuple[int, int], color: Color):
        if not self.at(coordinates).is_empty():
            raise OccupiedFieldMoveError

        bp_copy = deepcopy(self)
        bp_copy.set_field(coordinates, color)

        for neighbor_coordinate in bp_copy.neighbors(coordinates):
            if not bp_copy.at(neighbor_coordinate).is_empty() and bp_copy.at(
                    neighbor_coordinate).color == color.opposite():
                bp_copy = bp_copy.__kill_group_if_zero_liberties(neighbor_coordinate)

        if bp_copy.liberties(coordinates) == 0:
            raise SuicideMoveError

        return bp_copy

    def __kill_group_if_zero_liberties(self, coordinate: Tuple[int, int]):
        if not self.liberties(coordinate) == 0:
            return self
        for group_member_coordinates in self.group(coordinate):
            self.clear_field(group_member_coordinates)
        return self

    def __get_transl(self, val):
        if val == 0:
            return 1,
        elif val == self.size - 1:
            return -1,
        return -1, 1

    def __type_check(self, against):
        if not isinstance(against, BoardPosition):
            raise TypeError("can not compare BoardPosition to {}".format(type(against)))
        if not self.size == against.size:
            raise ValueError("can not compare BoardPosition of size {} with BoardPosition of size {}".format(
                self.size, against.size))

    def __check_coord(self, coord):
        if not isinstance(coord, tuple):
            raise TypeError("coord must be a tuple")
        if not len(coord) == 2:
            raise ValueError(
                "coord must be a tuple with exactly two elements")
        if coord not in self.__board_mask:
            raise IndexError("coord - index out of range")
