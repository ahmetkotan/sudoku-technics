from sudoku.mixins import DataMixin
from typing import List, Union, Tuple


class BaseSimplifier(DataMixin):
    data: List[List[int]]
    possibilities: List[List[Union[Tuple[int], int]]]
    size: int

    def __init__(
            self,
            initial_data: List[List[int]],
            possibilities: List[List[Union[Tuple[int, ...], int]]],
            size: int = 9,
    ):
        self.data = initial_data
        self.possibilities = possibilities
        self.size = size

    def simplify(self):
        raise NotImplementedError

    def run(self):
        while self.changed:
            self.simplify()
