from sudoku.simplifications.base import BaseSimplifier
from itertools import combinations
from typing import List, Union, Tuple, Generator


class HiddenDoubleSimplification(BaseSimplifier):
    def find_hidden_doubles(
        self, numbers: List[Union[Tuple[int, ...], int]]
    ) -> Generator[Tuple[int, Tuple[int, int]], None, None]:
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
                f"Simplify Hidden Double {row_no + 1}.row {col_no + 1}.column with {double}."
                f"Old: {self.possibilities[row_no][col_no]}"
            )
            self.possibilities[row_no][col_no] = double

    def simplify_column(self, col_no: int):
        numbers = self.get_column(col_no=col_no, possibilities=True)
        for row_no, double in self.find_hidden_doubles(numbers=numbers):
            print(
                f"Simplify Hidden Double {row_no + 1}.row {col_no + 1}.column with {double}."
                f"Old: {self.possibilities[row_no][col_no]}"
            )
            self.possibilities[row_no][col_no] = double

    def simplify_group(self, group_no: int):
        start_row = int(group_no / 3) * 3
        start_col = (group_no % 3) * 3
        numbers = self.get_group(row_no=start_row, col_no=start_col, possibilities=True, as_list=True)
        for cell_no, double in self.find_hidden_doubles(numbers=numbers):
            row_no = start_row + int(cell_no / 3)
            col_no = start_col + cell_no % 3
            print(
                f"Simplify Hidden Double {row_no + 1}.row {col_no + 1}.column with {double}."
                f"Old: {self.possibilities[row_no][col_no]}"
            )
            self.possibilities[row_no][col_no] = double
