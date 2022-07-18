# Standard Library
from math import sqrt
from typing import Set, List, Tuple, Union, Callable

# Sudoku Stuff
from sudoku.utils import chunks
from sudoku.simplifications.base import BaseSimplifier


class ReductionSimplification(BaseSimplifier):
    group_size: int

    def __init__(
        self,
        initial_data: List[List[int]],
        possibilities: List[List[Union[Tuple[int, ...], int]]],
        size: int = 9,
        callback: Callable = None,
    ):
        super().__init__(
            initial_data=initial_data,
            possibilities=possibilities,
            size=size,
            callback=callback,
        )
        self.group_size = int(sqrt(self.size))

    def simplify_row(self, row_no: int):
        pass

    def simplify_column(self, col_no: int):
        pass

    def find_row_in_sub_groups(
        self,
        number: int,
        numbers: List[Union[Tuple[int, ...], int]],
        line_type: str = "row",
    ) -> Set[int]:
        sub_groups = set()
        for cell_no, cell in enumerate(numbers):
            if not isinstance(cell, tuple):
                continue
            if number in cell:
                sub_groups.add(int(cell_no / self.group_size) if line_type == "row" else cell_no % self.group_size)

        return sub_groups

    def check_and_simplify_cell(
        self,
        original_group_no: int,
        row_no: int,
        col_no: int,
        cell: Union[Tuple[int, ...], int],
        number: int,
    ):
        if not isinstance(cell, tuple):
            return
        group_no = int(col_no / self.group_size) + (int(row_no / self.group_size) * 3)
        if group_no != original_group_no and number in cell:
            remaining = set(cell) - {number}
            if remaining != set(cell):
                self.console.print(
                    f"Simplified Line Reduction {row_no + 1}.row {col_no + 1}.column with {number}. "
                    f"Old: {self.possibilities[row_no][col_no]}"
                )
                self.possibilities[row_no][col_no] = tuple(sorted(remaining))
                self.changed = True

    def clear_row(self, original_group_no: int, number: int, row_no: int):
        for col_no, cell in enumerate(self.get_row(row_no=row_no, possibilities=True)):
            self.check_and_simplify_cell(
                original_group_no=original_group_no,
                row_no=row_no,
                col_no=col_no,
                cell=cell,
                number=number,
            )

    def clear_column(self, original_group_no: int, number: int, col_no: int):
        for row_no, cell in enumerate(self.get_column(col_no=col_no, possibilities=True)):
            self.check_and_simplify_cell(
                original_group_no=original_group_no,
                row_no=row_no,
                col_no=col_no,
                cell=cell,
                number=number,
            )

    def simplify_group(self, group_no: int):
        start_row = int(group_no / 3) * 3
        start_col = (group_no % 3) * 3
        numbers = self.get_group(row_no=start_row, col_no=start_col, possibilities=True, as_list=True)
        keys = set([x for p in numbers if isinstance(p, tuple) for x in p])
        for key in keys:
            sub_groups = self.find_row_in_sub_groups(number=key, numbers=numbers)
            if len(sub_groups) == 1:
                sub_group_no = sub_groups.pop()
                self.clear_row(
                    original_group_no=group_no,
                    number=key,
                    row_no=start_row + sub_group_no,
                )
            sub_groups = self.find_row_in_sub_groups(number=key, numbers=numbers, line_type="column")
            if len(sub_groups) == 1:
                sub_group_no = sub_groups.pop()
                self.clear_column(
                    original_group_no=group_no,
                    number=key,
                    col_no=start_col + sub_group_no,
                )
