from copy import deepcopy

from gologic.board.boardposition import BoardPosition


class State:
    def __init__(self, prev_pos: BoardPosition, now_pos: BoardPosition, b_captured: int = 0, w_captured: int = 0):

        self.__test_prev_and_now_pos(prev_pos, now_pos)

        self.__prev_pos = deepcopy(prev_pos)
        self.__now_pos = deepcopy(now_pos)

        self.__test_for_non_negativity(b_captured, 'b_captured')
        self.__b_captured = b_captured

        self.__test_for_non_negativity(w_captured, 'w_captured')
        self.__w_captured = w_captured

    @property
    def initial(self) -> bool:
        return self.__prev_pos.empty and self.__now_pos.empty

    @property
    def prev_position(self) -> BoardPosition:
        return self.__prev_pos

    @property
    def position(self) -> BoardPosition:
        return self.__now_pos

    @property
    def captured_black_stones(self):
        return self.__b_captured

    @property
    def captured_white_stones(self):
        return self.__w_captured

    def legal_moves(self):
        pass

    @classmethod
    def initial_state(cls, size):
        return cls(prev_pos=BoardPosition(size), now_pos=BoardPosition(size))

    @staticmethod
    def __test_for_non_negativity(val, name):
        if val < 0:
            raise ValueError(
                f"{name} must be a positive integer!"
            )

    @staticmethod
    def __test_prev_and_now_pos(prev_pos, now_pos):
        if not prev_pos.size == now_pos.size:
            raise TypeError("prev_pos and now_pos have to have same size")

        if not prev_pos.empty and now_pos.empty:
            raise TypeError("if now_pos is empty, prev_pos have to be empty also")

    def __eq__(self, other):
        if not isinstance(other, State):
            raise TypeError(
                f"can not compare State object with {type(other)}"
            )

        pos_eq = self.position == other.position and self.prev_position == other.prev_position
        captured_black_eq = self.captured_black_stones == other.captured_black_stones
        captured_white_eq = self.captured_white_stones == other.captured_white_stones

        return pos_eq and captured_black_eq and captured_white_eq