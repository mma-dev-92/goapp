from ..board.color import Color


class IllegalMoveError(Exception):
    pass


class SuicideMoveError(IllegalMoveError):
    pass


class OccupiedFieldMoveError(IllegalMoveError):
    pass


class State:
    def __init__(self):
        pass

    def calculate_next_state(self, color, coords):
        pass

    def illegal_moves_mask(self):
        pass
