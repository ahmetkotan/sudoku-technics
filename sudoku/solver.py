from copy import deepcopy
from typing import List

from sudoku.mixins import DataMixin
from sudoku.technics.singles import FillSingles


class Sudoku(DataMixin):
    methods = [FillSingles]

    def __init__(self, initial_data: List[List[int]] = None, size: int = 9):
        self.data = initial_data or []
        self.possibilities = deepcopy(initial_data)
        self.size = size

    def set_data(self, initial_data: List[List[int]]):
        self.data = initial_data
        self.possibilities = deepcopy(initial_data)

    def fill_possibilities(self) -> bool:
        changed = False
        tmp_changed = True

        while tmp_changed:
            tmp_changed = False
            for row_no, line in enumerate(self.data):
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
                        raise Exception("Error.")
                    elif len(possibilities) == 1:
                        print(
                            f"Found one possibility. Changed {row_no + 1}.row {col_no + 1}.columns with {possibilities[0]}"
                        )
                        self.data[row_no][col_no] = possibilities[0]
                        self.possibilities[row_no][col_no] = possibilities[0]
                        tmp_changed = True
                        changed = True
                    else:
                        self.possibilities[row_no][col_no] = tuple(possibilities)

        return changed

    def run_technics(self, results: List[bool]):
        for method_class in self.methods:
            method = method_class(initial_data=self.data, possibilities=self.possibilities)
            results.append(method.run())

    def solve(self):
        result = [self.fill_possibilities()]
        self.run_technics(results=result)

        while any(result):
            result = [self.fill_possibilities()]
            self.run_technics(results=result)
