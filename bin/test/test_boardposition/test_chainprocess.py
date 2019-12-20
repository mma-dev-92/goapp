from random import randrange
import unittest

from ...gologic.board.boardposition import ChainProcess, StartConditions, Conditions


class TestChainProcess(unittest.TestCase):
    def test_1_dimentional_list_len(self):
        l = list(range(10))

        start_cond = StartConditions(value=0, position=0)
        conditions = Conditions(
            adjacent=lambda pos: [pos + 1] if pos + 1 < len(l) else [],
            stop_before=lambda pos: False,
            stop_after=lambda pos: False,
        )
        def step(value, pos): return value + 1

        process = ChainProcess(start_cond, conditions, step)

        result = process.run()
        expected_result = len(l)

        self.assertEqual(result, expected_result)

    def test_2_dim_list_volume(self):
        n = 10
        dim2 = list(list(range(n) for _ in range(n)))

        start_cond = StartConditions(value=0, position=(0, 0))

        def next_pos(pos):
            x, y = pos
            if y == n - 1 and x == n - 1:
                return []
            if y == n - 1:
                return [(x + 1, 0)]
            return [(x, y + 1)]

        conditions = Conditions(
            adjacent=next_pos,
            stop_before=lambda pos: False,
            stop_after=lambda pos: False
        )

        def step(value, pos): return value + 1

        process = ChainProcess(start_cond, conditions, step)

        result = process.run()
        expected_result = len(dim2) ** 2
        self.assertEqual(result, expected_result)
