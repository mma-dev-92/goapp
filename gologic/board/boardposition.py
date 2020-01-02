from __future__ import annotations
from itertools import product
from typing import TypeVar, Callable, Tuple

from gologic.board.field import Field, EmptyField, NonEmptyField


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

    def bind(self, f, e, start_coord, stop_before=lambda x: False, stop_after=lambda x: False):
        visited, to_visit, result = {coord: False for coord in self.coords}, set([start_coord]), e
        while to_visit:
            v = to_visit.pop()
            if not stop_before(v):
                result = f(result, v)
                if not stop_after(v):
                    to_visit.update([nv for nv in self.neighbours(v) if not visited[nv]])
            visited[v] = True
        return result

    def liberties(self, coord):
        if self.at(coord).is_empty():
            raise RuntimeError("Trying to count liberties of an empty field")

        def f(val, _coord):
            return val + 1 if self.at(_coord).is_empty() else val

        def stop_before(_coord):
            return not self.at(_coord).is_empty() and not self.at(coord).color == self.at(_coord).color

        def stop_after(_coord):
            return self.at(_coord).is_empty()

        return self.bind(f=f, e=0, start_coord=coord, stop_before=stop_before, stop_after=stop_after)

    def group(self, coord):
        if self.at(coord).is_empty():
            return []

        def f(val, _coord):
            return val + [_coord] if self.at(_coord) == self.at(coord) else val

        def stop_before(_coord):
            return not self.at(_coord) == self.at(coord)

        return self.bind(f=f, e=[], start_coord=coord, stop_before=stop_before)

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
            raise IndexError("BoardPosition coord - index out of range")

    def __check_size(self, size):
        if not isinstance(size, int):
            raise TypeError("size must be an int")
        if size not in self.__VALID_SIZES:
            raise ValueError("size must be one of {}".format(self.__VALID_SIZES))
