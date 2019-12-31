from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
import colorama
from termcolor import colored

from gologic.board.color import Color


class Field(ABC):
    @abstractmethod
    def is_empty(self):
        pass

    @abstractmethod
    def is_black(self):
        pass

    @abstractmethod
    def is_white(self):
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

    def color_print(self):
        return colored('o', 'grey', 'on_cyan', attrs=['blink']) if self.color == Color.BLACK else colored(
            'o', 'white', 'on_cyan', attrs=['blink'])


class EmptyField(Field):
    def is_empty(self):
        return True

    def color(self):
        return None

    def color_print(self):
        return colored('+', 'yellow', 'on_cyan', attrs=['blink'])

    def is_white(self):
        return False

    def is_black(self):
        return False
