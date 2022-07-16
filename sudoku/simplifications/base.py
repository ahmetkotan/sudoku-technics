from sudoku.mixins import DataMixin
from typing import List, Union, Tuple, Callable


class BaseSimplifier(DataMixin):
    data: List[List[int]]
    possibilities: List[List[Union[Tuple[int], int]]]
    size: int
    callback: Callable

    def __init__(
            self,
            initial_data: List[List[int]],
            possibilities: List[List[Union[Tuple[int, ...], int]]],
            size: int = 9,
            callback: Callable = None,
    ):
        self.data = initial_data
        self.possibilities = possibilities
        self.size = size
        self.callback = callback

    def simplify_row(self, row_no: int):
        raise NotImplementedError

    def simplify_column(self, col_no: int):
        raise NotImplementedError

    def simplify_group(self, group_no: int):
        raise NotImplementedError

    def simplify(self):
        changed = False
        for n in range(self.size):
            self.changed = False
            self.simplify_row(row_no=n)
            changed = self.changed or changed

        for n in range(self.size):
            self.changed = False
            self.simplify_column(col_no=n)
            changed = self.changed or changed

        for n in range(self.size):
            self.changed = False
            self.simplify_group(group_no=n)
            changed = self.changed or changed

        if changed and self.callback:
            self.callback()

    def run(self):
        self.simplify()
