from typing import List, Tuple, Union

from sudoku.mixins import DataMixin


class BaseTechnic(DataMixin):
    data: List[List[int]]
    possibilities: List[List[Union[Tuple[int], int]]]
    size: int

    def __init__(self, initial_data: List[List[int]], possibilities: List[List[Union[Tuple[int], int]]], size: int = 9):
        self.data = initial_data
        self.possibilities = possibilities
        self.size = size

    def run(self):
        raise NotImplemented
