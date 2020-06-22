from __future__ import annotations
from enum import Enum


class Color(Enum):
    BLACK = 1
    WHITE = 2

    def opposite(self):
        return Color.WHITE if self.name == 'BLACK' else Color.BLACK

    def __eq__(self, other):
        if not isinstance(other, Color):
            raise TypeError("can not compare color object to {} object".format(type(other)))
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)
