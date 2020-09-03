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

    @property
    def initial(self) -> bool:
        pass

    def legal_moves(self):
        pass

    @staticmethod
    def initial_state(self):
        pass

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
