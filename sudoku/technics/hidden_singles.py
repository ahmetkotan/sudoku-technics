from typing import List, Tuple, Union, Dict
from sudoku.technics.base import BaseTechnic


class HiddenSingles(BaseTechnic):
    @staticmethod
    def find_hidden_singles(numbers: List[int], counts: Dict[int, int]):
        for no, number in enumerate(numbers):
            if isinstance(number, tuple):
                for n in number:
                    if counts[n] == 1:
                        yield no, n

    def find_hidden_singles_in_row(self, row_no: int):
        numbers = self.get_row(row_no=row_no, possibilities=True)
        counts = self.get_possibilities_counts(numbers=numbers)
        for col_no, number in self.find_hidden_singles(numbers=numbers, counts=counts):
            self.data[row_no][col_no] = number
            self.possibilities[row_no][col_no] = number
            print(
                f"Found hidden single in row. Changed {row_no + 1}.row {col_no + 1}.columns with {number}"
            )
            return self.callback()

    def find_hidden_singles_in_column(self, col_no: int):
        numbers = self.get_column(col_no=col_no, possibilities=True)
        counts = self.get_possibilities_counts(numbers=numbers)
        for row_no, number in self.find_hidden_singles(numbers=numbers, counts=counts):
            self.data[row_no][col_no] = number
            self.possibilities[row_no][col_no] = number
            print(
                f"Found hidden single in column. Changed {row_no + 1}.row {col_no + 1}.columns with {number}"
            )
            return self.callback()

    def find_hidden_singles_in_group(self, group_no: int):
        start_row = int(group_no / 3) * 3
        start_col = (group_no % 3) * 3
        numbers = self.get_group(
            row_no=start_row, col_no=start_col, possibilities=True, as_list=True
        )
        counts = self.get_possibilities_counts(numbers=numbers)
        for cell_no, number in self.find_hidden_singles(numbers=numbers, counts=counts):
            row_no = start_row + int(cell_no / 3)
            col_no = start_col + cell_no % 3
            self.data[row_no][col_no] = number
            self.possibilities[row_no][col_no] = number
            print(
                f"Found hidden single in group. Changed {row_no + 1}.row {col_no + 1}.columns with {number}"
            )
            return self.callback()

    def run(self):
        for n in range(self.size):
            self.find_hidden_singles_in_row(row_no=n)

        for n in range(self.size):
            self.find_hidden_singles_in_column(col_no=n)

        for n in range(self.size):
            self.find_hidden_singles_in_group(group_no=n)
