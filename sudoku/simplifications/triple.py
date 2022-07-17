# Standard Library
from itertools import combinations
from typing import List, Tuple, Union, Generator

# Sudoku Stuff
from sudoku.simplifications.base import BaseSimplifier


class TripleSimplification(BaseSimplifier):
    @staticmethod
    def find_triples(numbers: List[Union[Tuple[int, ...], int]]) -> Generator[Tuple[int, int, int], None, None]:
        possibilities = [cell for cell in numbers if isinstance(cell, tuple)]
        keys = set([x for cell in possibilities for x in cell])
        options = combinations(keys, 3)
        for option in options:
            x, y, z = sorted(option)
            results = [(x, y) in numbers, (x, z) in numbers, (y, z) in numbers, (x, y, z) in numbers]
            if results.count(True) == 3:
                yield x, y, z

    def simplify_numbers(
        self, numbers: List[Union[Tuple[int, ...], int]]
    ) -> Generator[Tuple[int, Tuple[int, ...]], None, None]:
        for triple in self.find_triples(numbers=numbers):
            for cell_no, cell in enumerate(numbers):
                if not isinstance(cell, tuple) or triple == cell:
                    continue
                remaining = tuple(sorted(set(cell) - set(triple)))
                if remaining and remaining != cell:
                    self.changed = True
                    yield cell_no, remaining

    def simplify_row(self, row_no: int):
        numbers = self.get_row(row_no=row_no, possibilities=True)
        for col_no, remaining in self.simplify_numbers(numbers=numbers):
            print(
                f"Simplify Triple {row_no + 1}.row {col_no + 1}.column with {remaining}."
                f"Old: {self.possibilities[row_no][col_no]}"
            )
            self.possibilities[row_no][col_no] = remaining

    def simplify_column(self, col_no: int):
        numbers = self.get_column(col_no=col_no, possibilities=True)
        for row_no, remaining in self.simplify_numbers(numbers=numbers):
            print(
                f"Simplify Triple {row_no + 1}.row {col_no + 1}.column with {remaining}."
                f"Old: {self.possibilities[row_no][col_no]}"
            )
            self.possibilities[row_no][col_no] = remaining

    def simplify_group(self, group_no: int):
        start_row = int(group_no / 3) * 3
        start_col = (group_no % 3) * 3
        numbers = self.get_group(row_no=start_row, col_no=start_col, possibilities=True, as_list=True)
        for cell_no, remaining in self.simplify_numbers(numbers=numbers):
            row_no = start_row + int(cell_no / 3)
            col_no = start_col + cell_no % 3
            print(
                f"Simplify Triple {row_no + 1}.row {col_no + 1}.column with {remaining}."
                f"Old: {self.possibilities[row_no][col_no]}"
            )
            self.possibilities[row_no][col_no] = remaining
