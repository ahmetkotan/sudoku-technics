from collections import defaultdict
from typing import List, Union, Tuple

from sudoku.simplifications.base import BaseSimplifier


class DoublesSimplification(BaseSimplifier):
    @staticmethod
    def find_pairs(numbers: List[int]):
        pairs = defaultdict(lambda: 0)
        for cell in numbers:
            if isinstance(cell, tuple):
                if len(cell) == 2:
                    pairs[cell] += 1

        return [pair for pair, count in pairs.items() if count == 2]

    def simplify_numbers(self, numbers: List[Union[Tuple[int, ...], int]]):
        for pair in self.find_pairs(numbers=numbers):
            for cell_no, cell in enumerate(numbers):
                if not isinstance(cell, tuple) or pair == cell:
                    continue
                remaining = tuple(sorted(set(cell) - set(pair)))
                if remaining and remaining != cell:
                    self.changed = True
                    yield cell_no, remaining

    def simplify_row(self, row_no: int):
        numbers = self.get_row(row_no=row_no, possibilities=True)
        for col_no, remaining in self.simplify_numbers(numbers=numbers):
            print(f"Simplify Double in Row {row_no + 1}.row {col_no + 1}.column with {remaining}. Old: {self.possibilities[row_no][col_no]}")
            self.possibilities[row_no][col_no] = remaining

    def simplify_column(self, col_no: int):
        numbers = self.get_column(col_no=col_no, possibilities=True)
        for row_no, remaining in self.simplify_numbers(numbers=numbers):
            print(
                f"Simplify Double in Column {row_no + 1}.row {col_no + 1}.column with {remaining}. Old: {self.possibilities[row_no][col_no]}")
            self.possibilities[row_no][col_no] = remaining

    def simplify_group(self, group_no: int):
        start_row = int(group_no / 3) * 3
        start_col = (group_no % 3) * 3
        numbers = self.get_group(
            row_no=start_row, col_no=start_col, possibilities=True, as_list=True
        )
        for cell_no, remaining in self.simplify_numbers(numbers=numbers):
            row_no = start_row + int(cell_no / 3)
            col_no = start_col + cell_no % 3
            print(
                f"Simplify Double in Group {row_no + 1}.row {col_no + 1}.column with {remaining}. Old: {self.possibilities[row_no][col_no]}")
            self.possibilities[row_no][col_no] = remaining
