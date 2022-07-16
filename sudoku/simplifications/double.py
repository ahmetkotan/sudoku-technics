from collections import defaultdict
from typing import List

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

    def simplify_row(self, row_no: int):
        numbers = self.get_row(row_no=row_no, possibilities=True)
        for pair in self.find_pairs(numbers=numbers):
            for col_no, cell in enumerate(numbers):
                if not isinstance(cell, tuple) or pair == cell:
                    continue
                remaining = set(cell) - set(pair)
                print(f"Simplified doubles in {row_no + 1}.row with {pair}. Remaining: {remaining}")
                new_possibilities = tuple(sorted(remaining))
                if new_possibilities != cell:
                    self.possibilities[row_no][col_no] = tuple(sorted(remaining))

    def simplify_column(self, col_no: int):
        numbers = self.get_column(col_no=col_no, possibilities=True)
        for pair in self.find_pairs(numbers=numbers):
            for row_no, cell in enumerate(numbers):
                if not isinstance(cell, tuple) or pair == cell:
                    continue
                remaining = set(cell) - set(pair)
                print(f"Simplified doubles in {col_no + 1}.column with {pair}. Remaining: {remaining}")
                new_possibilities = tuple(sorted(remaining))
                if new_possibilities != cell:
                    self.possibilities[row_no][col_no] = tuple(sorted(remaining))
                    self.changed = True

    def simplify_group(self, group_no: int):
        start_row = int(group_no / 3) * 3
        start_col = (group_no % 3) * 3
        numbers = self.get_group(
            row_no=start_row, col_no=start_col, possibilities=True, as_list=True
        )
        for pair in self.find_pairs(numbers=numbers):
            for cell_no, cell in enumerate(numbers):
                if not isinstance(cell, tuple) or pair == cell:
                    continue
                row_no = start_row + int(cell_no / 3)
                col_no = start_col + cell_no % 3
                remaining = set(cell) - set(pair)
                print(f"Simplified doubles in {group_no + 1}.group with {pair}. Remaining: {remaining}")
                new_possibilities = tuple(sorted(remaining))
                if new_possibilities != cell:
                    self.possibilities[row_no][col_no] = tuple(sorted(remaining))
                    self.changed = True

    def simplify(self):
        for n in range(self.size):
            self.simplify_row(row_no=n)

        for n in range(self.size):
            self.changed = False
            self.simplify_column(col_no=n)

        for n in range(self.size):
            self.changed = False
            self.simplify_group(group_no=n)

