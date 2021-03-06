from random import randint

from test.utils.base import BaseTestCaseClass


# TODO: refactor it... it is ugly...

class TestBind(BaseTestCaseClass):
    def test_count_empty_fields_on_empty_board(self):
        bp = self.random_size_empty_board()
        size = bp.size
        expected_result = size ** 2
        result = bp.bind(operation=lambda val, coord: val + 1, neutral_elem=0, start_coord=(0, 0))
        self.assertEqual(result, expected_result,
                         msg=self.error_msg(bp, "count_empty_fields", result, expected_result))

    def test_count_black_stones_on_random_board(self):
        bp = self.random_size_empty_board()
        black_stones = randint(0, bp.size - 1)
        random_coordinates = self.random_coordinates(
            bp.size, black=black_stones, white=bp.size ** 2 - black_stones)
        bp = self.fill(bp, random_coordinates)
        result = bp.bind(operation=lambda val, coord: val + 1 if bp.at(coord).is_black()
                         else val, neutral_elem=0, start_coord=(0, 0))
        self.assertEqual(result, black_stones,
                         msg=self.error_msg(bp, "count_black_stones", result, black_stones))

    def test_sum_empty_fields_on_random_board(self):
        bp = self.random_size_empty_board()
        bp = self.fill(bp, self.random_coordinates(bp.size, black=5, white=5))

        expected_result = sum(range(bp.size ** 2 - 10))
        result = bp.bind(operation=lambda val, coord: (val[0] + 1, val[1] + val[0]) if bp.at(coord).is_empty()
                         else val, neutral_elem=(0, 0), start_coord=(0, 0))
        self.assertEqual(expected_result, result[1],
                         msg=self.error_msg(bp, "sum_empty_fields", result[1], expected_result))
