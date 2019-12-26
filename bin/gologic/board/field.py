from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum

from .color import Color


class Field(ABC):
    @abstractmethod
    def is_empty(self):
        pass

    def __eq__(self, other):
        if not isinstance(other, Field):
            raise TypeError(
                "can not compare {} to type {}".format(
                    Field, type(other)))
        if self.is_empty() and other.is_empty():
            return True
        elif not self.is_empty() == other.is_empty():
            return False
        return self.color == other.color

    @abstractmethod
    def is_black(self):
        pass

    @abstractmethod
    def is_white(self):
        pass


class NonEmptyField(Field):
    def __init__(self, color):
        if not isinstance(color, Color):
            raise TypeError(
                "color must have type {}".format(Color))
        self.__color = color

    @property
    def color(self):
        return self.__color

    def is_black(self):
        return self.color == Color.BLACK

    def is_white(self):
        return self.color == Color.WHITE

    def is_empty(self):
        return False

    def __str__(self):
        return self.color.name[0]


class EmptyField(Field):
    def is_empty(self):
        return True

    def __str__(self):
        return 'E'

    def is_white(self):
        return False

    def is_black(self):
        return False
