from typing import List, Tuple, Union, Dict
from collections import defaultdict

from sudoku.getters import (
    get_column,
    get_group,
    get_row,
    has_in_column,
    has_in_group,
    has_in_row,
)


class DataMixin:
    data: List[List[int]]
    possibilities: List[List[Union[Tuple[int], int]]]
    size: int
    changed: bool = True

    def get_data(self) -> List[List[int]]:
        return self.data

    def get_possibilities(self) -> List[List[Union[Tuple[int], int]]]:
        return self.possibilities

    def print_data(self, with_rows: bool = False):
        for n, line in enumerate(self.data):
            print(f"{n if with_rows else ''} {line}")

    def print_possibilities(self, with_rows: bool = False):
        for n, line in enumerate(self.possibilities):
            print(f"{n if with_rows else ''} {line}")

    def has_in_row(self, row: int, number: int) -> bool:
        return has_in_row(row_no=row, number=number, data=self.data)

    def find_in_row(self, row: int, number: int) -> int:
        if self.has_in_row(row=row, number=number):
            return self.data[row].index(number)
        return -1

    def find_in_column(self, column: int, number: int) -> int:
        for line_number, line in enumerate(self.data):
            if number == line[column]:
                return line_number
        return -1

    def has_in_column(self, column: int, number: int) -> bool:
        return has_in_column(column=column, number=number, data=self.data)

    def get_row(self, row_no: int, possibilities: bool = False) -> List[int]:
        return get_row(
            row_no=row_no, data=self.possibilities if possibilities else self.data
        )

    def get_column(self, col_no: int, possibilities: bool = False) -> List[int]:
        return get_column(
            col_no=col_no, data=self.possibilities if possibilities else self.data
        )

    def get_group(
        self,
        row_no: int,
        col_no: int,
        possibilities: bool = False,
        as_list: bool = False,
    ) -> Union[List[List[int]], List[int]]:
        group = get_group(
            row_no=row_no,
            col_no=col_no,
            data=self.possibilities if possibilities else self.data,
        )
        if as_list:
            numbers: List[int] = []
            for line in group:
                numbers.extend(line)
            return numbers

        return group

    def has_in_group(self, row_no: int, col_no: int, number: int) -> bool:
        return has_in_group(row_no=row_no, col_no=col_no, number=number, data=self.data)

    @staticmethod
    def get_possibilities_counts(
        numbers: List[Union[Tuple[int], int]]
    ) -> Dict[int, int]:
        counts = defaultdict(lambda: 0)
        for number in numbers:
            if isinstance(number, tuple):
                for n in number:
                    counts[n] += 1

        return counts
