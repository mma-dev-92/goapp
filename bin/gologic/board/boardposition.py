from __future__ import annotations
from itertools import product
from collections import namedtuple
from pprint import pprint

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

    def liberties(self, coord):
        pass

    def group(self, coord):
        pass

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
            print(coord)
            raise IndexError("BoardPosition coord - index out of range")

    def __check_size(self, size):
        if not isinstance(size, int):
            raise TypeError("size must be an int")
        if size not in self.__VALID_SIZES:
            raise ValueError("size must be one of {}".format(self.__VALID_SIZES))


StartConditions = namedtuple('StartConditions', ['value', 'position'])

Conditions = namedtuple('Conditions', ['adjacent', 'stop_before', 'stop_after'])


class ChainProcess:

    def __init__(self, start_cond: StartConditions, conditions: Conditions, step):
        self.__init_state(start_cond)
        self.__conditions = conditions
        self.__step = step

    def run(self):
        while self.to_visit:
            self.__process()
        return self.value

    def __init_state(self, start_cond):
        self.value = start_cond.value
        self.visited = dict()
        self.to_visit = [start_cond.position]

    def __process(self):
        coord = self.to_visit.pop()
        if not self.__conditions.stop_before(coord):
            self.__process_cord(coord)
            if not self.__conditions.stop_after(coord):
                self.to_visit.extend(self.__adjacent_coords(coord))

    def __process_cord(self, coord):
        self.visited[coord] = True
        self.value = self.__step(self.value, coord)

    def __adjacent_coords(self, coord):
        return [nv for nv in self.__conditions.adjacent(
            coord) if nv not in self.visited and nv not in self.to_visit]
