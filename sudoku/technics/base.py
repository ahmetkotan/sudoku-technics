from typing import List, Tuple, Union, Callable

from sudoku.mixins import DataMixin


class BaseTechnic(DataMixin):
    data: List[List[int]]
    possibilities: List[List[Union[Tuple[int], int]]]
    size: int
    callback: Callable

    def __init__(
        self,
        initial_data: List[List[int]],
        possibilities: List[List[Union[Tuple[int], int]]],
        size: int = 9,
        callback: Callable = None,
    ):
        self.data = initial_data
        self.possibilities = possibilities
        self.size = size
        self.callback = callback

    def run(self):
        raise NotImplemented
