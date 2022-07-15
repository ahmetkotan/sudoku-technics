from copy import deepcopy
from typing import List

from sudoku.mixins import DataMixin
from sudoku.technics.singles import HiddenSingles
from sudoku.technics.bowman import BowmanBingo


class Sudoku(DataMixin):
    methods = [HiddenSingles, BowmanBingo]
    changed: bool = True

    def __init__(self, initial_data: List[List[int]] = None, size: int = 9):
        self.data = initial_data or []
        self.possibilities = deepcopy(initial_data)
        self.size = size

    def set_data(self, initial_data: List[List[int]]):
        self.data = initial_data
        self.possibilities = deepcopy(initial_data)

    def run_technics(self):
        def callback():
            self.solve()

        for method_class in self.methods:
            method = method_class(initial_data=self.data, possibilities=self.possibilities, callback=callback)
            method.run()

    def solve(self):
        self.reload_possibilities()
        self.run_technics()
