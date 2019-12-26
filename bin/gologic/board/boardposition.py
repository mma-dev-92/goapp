from __future__ import annotations
from itertools import product
from collections import namedtuple
from pprint import pprint
from typing import TypeVar, Callable, Tuple

from .field import Field, EmptyField, NonEmptyField


class BoardPosition:

    __VALID_SIZES = [9, 13, 19]

    def __init__(self, size):
        self.__check_size(size)
        self.__size = size
        self.__board_mask = {coord: EmptyField()
                             for coord in product(range(size), range(size))}

    @property
    def size(self):
        return self.__size

    @property
    def coords(self):
        return self.__board_mask.keys()

    def clear(self):
        for coord in self.__board_mask:
            self.__board_mask[coord] = EmptyField()

    def at(self, coord):
        self.__check_coord(coord)
        return self.__board_mask[coord]

    def set_field(self, coord, color):
        self.__check_coord(coord)
        self.__board_mask[coord] = NonEmptyField(color)

    def clear_field(self, coord):
        self.__check_coord(coord)
        self.__board_mask[coord] = EmptyField()

    def __eq__(self, other):
        self.__typecheck(against=other)
        return self.__board_mask == other.__board_mask

    T = TypeVar('T')

    def bind(self, f: Callable[[T, Tuple[int, int]], T], e: T, start_coord: Tuple[int, int], stop_before: Callable[[
             Tuple[int, int]], bool] = lambda x: False, stop_after: Callable[[Tuple[int, int]], bool] = lambda x: False) -> T:
        to_visit, result = [start_coord], e
        visited = {coord: False for coord in self.coords}
        while to_visit:
            v = to_visit.pop()
            visited[v] = True
            if not stop_before(v):
                result = f(result, v)
                if not stop_after(v):
                    vrtcs_to_add = [nv for nv in self.neighbours(v) if not visited[nv] and not nv in to_visit]
                    to_visit.extend(vrtcs_to_add)
        return result

    def liberties(self, coord):
        pass

    def group(self, coord):
        if self.at(coord).is_empty():
            return []
        return self.bind(f=lambda val, _coord: val + [_coord] if self.at(_coord) == self.at(coord) else val,
                         e=[], start_coord=coord, stop_before=lambda _coord: not self.at(_coord) == self.at(coord))

    def neighbours(self, coord):
        row, col = coord
        return [(row + rt, col) for rt in self.__get_transl(row)] + \
            [(row, col + ct) for ct in self.__get_transl(col)]

    def __get_transl(self, val):
        if val == 0:
            return (1,)
        elif val == self.size - 1:
            return (-1,)
        return (-1, 1)

    def __typecheck(self, against):
        if not isinstance(against, BoardPosition):
            raise TypeError("can not compare BoardPosition to {}".format(type(against)))
        if not self.size == against.size:
            raise ValueError("can not compare BoardPosition of size {} with BoardPosition of size {}".format(
                self.size, against.size))

    def __check_coord(self, coord):
        if not isinstance(coord, tuple):
            raise TypeError("BoardPosition coord must be a tuple")
        if not len(coord) == 2:
            raise ValueError(
                "BoardPosition coord must be a tuple with exactly two elements")
        if not coord in self.__board_mask:
            pprint(self.size)
            raise IndexError("BoardPosition coord - index out of range")

    def __check_size(self, size):
        if not isinstance(size, int):
            raise TypeError("size must be an int")
        if size not in self.__VALID_SIZES:
            raise ValueError("size must be one of {}".format(self.__VALID_SIZES))
