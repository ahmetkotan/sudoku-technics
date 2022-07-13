from typing import List, Tuple, Union, Dict
from sudoku.technics.base import BaseTechnic


class FillSingles(BaseTechnic):
    def get_possibilities_counts(
        self, numbers: List[Union[Tuple[int], int]]
    ) -> Dict[int, int]:
        counts = {i: 0 for i in range(1, self.size + 1)}
        for number in numbers:
            if isinstance(number, tuple):
                for n in number:
                    counts[n] += 1

        return counts

    def find_hidden_singles_in_row(self, row_no: int) -> bool:
        changed = False
        numbers = self.get_row(row_no=row_no, possibilities=True)
        counts = self.get_possibilities_counts(numbers=numbers)
        for col_no, number in enumerate(numbers):
            if isinstance(number, tuple):
                for n in number:
                    if counts[n] == 1:
                        print(
                            f"Found a single in row. Changed {row_no + 1}.row {col_no + 1}.columns with {n}"
                        )
                        self.data[row_no][col_no] = n
                        self.possibilities[row_no][col_no] = n
                        changed = True

        return changed

    def run(self) -> bool:
        changed = False
        for n in range(self.size):
            if self.find_hidden_singles_in_row(row_no=n):
                changed = True

        return changed
