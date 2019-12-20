from __future__ import annotations
from enum import Enum


class Color(Enum):
    BLACK = 1
    WHITE = 2

    def oposite(self):
        return Color.WHITE if self.name == 'BLACK' else Color.WHITE
