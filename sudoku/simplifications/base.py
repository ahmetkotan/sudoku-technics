# Standard Library
from typing import List, Tuple, Union, Callable

# Third Party
from rich.style import Style
from rich.console import Console

# Sudoku Stuff
from sudoku.mixins import DataMixin


class BaseSimplifier(DataMixin):
    data: List[List[int]]
    possibilities: List[List[Union[Tuple[int], int]]]
    size: int
    callback: Callable
    console: Console = Console(style=Style(bold=True, color="blue"))

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
