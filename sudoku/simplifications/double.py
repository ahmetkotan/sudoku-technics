from collections import defaultdict

from sudoku.simplifications.base import BaseSimplifier


class DoublesSimplification(BaseSimplifier):
    def simplify_rows(self, row_no: int):
        pairs = defaultdict(lambda: 0)
        for col in self.get_row(row_no=row_no, possibilities=True):
            if isinstance(col, tuple):
                if len(col) == 2:
                    pairs[col] += 1

        for pair in [pair for pair, count in pairs.items() if count == 2]:
            for col_no, cell in enumerate(
                self.get_row(row_no=row_no, possibilities=True)
            ):
                if not isinstance(cell, tuple) or pair == cell:
                    continue
                left = set(cell) - set(pair)
                print(f"Simplified {row_no}.row {col_no}.column with {pair}")
                self.possibilities[row_no][col_no] = tuple(sorted(left))

    def run(self):
        for n in range(self.size):
            self.simplify_rows(row_no=n)
