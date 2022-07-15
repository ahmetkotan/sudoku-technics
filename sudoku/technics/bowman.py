from sudoku.technics.base import BaseTechnic
from typing import Tuple, List, Union
from copy import deepcopy
from sudoku.exceptions import BowmanFailedError
from collections import Counter


class BowmanBingo(BaseTechnic):
    def find_possibilities(self, count: int) -> Tuple[int, int]:
        for row_no, line in enumerate(self.possibilities):
            for cell_no, cell in enumerate(line):
                if isinstance(cell, tuple):
                    if len(cell) == 2:
                        yield row_no, cell_no

        return -1, -1

    def fill_temporary_possibilities(
        self, tmp_possibilities: List[List[Union[Tuple[int], int]]], tmp_data: List[List[int]],
    ):
        for row_no, line in enumerate(tmp_data):
            line_possibilities = set(range(0, self.size + 1)) - set(line)
            for col_no in range(self.size):
                if line[col_no] != 0:
                    continue

                possibilities = [
                    number
                    for number in line_possibilities
                    if not self.has_in_column(column=col_no, number=number)
                       and not self.has_in_group(
                        row_no=row_no, col_no=col_no, number=number
                    )
                ]
                if len(possibilities) == 0:
                    raise BowmanFailedError
                elif len(possibilities) == 1:
                    tmp_data[row_no][col_no] = possibilities[0]
                    tmp_possibilities[row_no][col_no] = possibilities[0]
                    return self.fill_temporary_possibilities(tmp_possibilities=tmp_possibilities, tmp_data=tmp_data)
                else:
                    tmp_possibilities[row_no][col_no] = tuple(possibilities)

    def try_possibilities(self, row_no: int, col_no: int):
        cell = self.possibilities[row_no][col_no]
        results = {i: True for i in cell}
        for number in cell:
            tmp_possibilities = deepcopy(self.possibilities)
            tmp_data = deepcopy(self.data)
            try:
                tmp_possibilities[row_no][col_no] = number
                tmp_data[row_no][col_no] = number
                self.fill_temporary_possibilities(tmp_possibilities=tmp_possibilities, tmp_data=tmp_data)
            except BowmanFailedError:
                results[number] = False

        counts = Counter(results.values())
        if counts[True] == 1:
            pick_number = cell[0] if results[cell[0]] else cell[1]
            self.data[row_no][col_no] = pick_number
            self.possibilities[row_no][col_no] = pick_number
            print(f"Found {row_no + 1}.row {col_no + 1}.column with Bowman's Bingo as {pick_number}")
            self.callback()

    def run(self):
        for count in range(2, self.size):
            for row_no, col_no in self.find_possibilities(count=count):
                if row_no == -1 or col_no == -1:
                    break
                self.try_possibilities(row_no=row_no, col_no=col_no)
