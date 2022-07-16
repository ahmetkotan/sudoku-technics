from sudoku.simplifications.base import BaseSimplifier
from itertools import combinations
from typing import List, Union, Tuple


class HiddenDoubleSimplification(BaseSimplifier):
    def find_hidden_doubles(self, numbers: List[Union[Tuple[int, ...], int]]):
        possibilities = [cell for cell in numbers if isinstance(cell, tuple)]
        keys = set([x for cell in possibilities for x in cell])
        counts = self.get_possibilities_counts(numbers=possibilities)
        options = combinations(keys, 2)
        for option in options:
            x, y = sorted(option)
            for cell_no, cell in enumerate(numbers):
                if not isinstance(cell, tuple):
                    continue
                if x in cell and y in cell and counts.get(x) == 2 and counts.get(y) == 2 and (x, y) != cell:
                    self.changed = True
                    yield cell_no, (x, y)

    def simplify_row(self, row_no: int):
        numbers = self.get_row(row_no=row_no, possibilities=True)
        for col_no, double in self.find_hidden_doubles(numbers=numbers):
            print(
                f"Simplify Hidden Double {row_no + 1}.row {col_no + 1}.column with {double}. Old: {self.possibilities[row_no][col_no]}")
            self.possibilities[row_no][col_no] = double

    def simplify_column(self, col_no: int):
        pass

    def simplify_group(self, group_no: int):
        pass
