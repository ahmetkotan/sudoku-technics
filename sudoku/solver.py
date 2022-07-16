from copy import deepcopy
from typing import List

from sudoku.mixins import DataMixin
from sudoku.technics.hidden_singles import HiddenSingles
from sudoku.technics.singles import Singles
from sudoku.technics.bowman import BowmanBingo
from sudoku.simplifications.double import DoublesSimplification
from sudoku.simplifications.triple import TripleSimplification
from sudoku.simplifications.hidden_double import HiddenDoubleSimplification


class Sudoku(DataMixin):
    methods = [HiddenSingles, Singles, BowmanBingo]
    simplifications = [DoublesSimplification, TripleSimplification, HiddenDoubleSimplification]

    changed: bool = True
    simplification_continue: bool = True

    def __init__(self, initial_data: List[List[int]] = None, size: int = 9):
        self.data = initial_data or []
        self.possibilities = deepcopy(initial_data)
        self.size = size

    def set_data(self, initial_data: List[List[int]]):
        self.data = initial_data
        self.possibilities = deepcopy(initial_data)

    def fill_possibilities(self):
        self.changed = False
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
                    self.print_possibilities()
                    raise Exception(f"Error in {row_no + 1}.row {col_no + 1}.column")
                else:
                    self.possibilities[row_no][col_no] = tuple(sorted(possibilities))

    def run_technics(self):
        def callback():
            self.solve()

        for method_class in self.methods:
            method = method_class(
                initial_data=self.data,
                possibilities=self.possibilities,
                callback=callback,
            )
            method.run()

    def run_simplifications(self):
        def callback():
            self.run_simplifications()

        for simplifier_class in self.simplifications:
            simplifier = simplifier_class(initial_data=self.data, possibilities=self.possibilities, callback=callback)
            simplifier.run()

    def solve(self):
        self.fill_possibilities()
        self.run_simplifications()
        self.run_technics()
