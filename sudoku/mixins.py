# Standard Library
from collections import defaultdict
from typing import Dict, List, Tuple, Union

# Third Party
from rich.style import Style
from rich.table import Table
from rich.console import Console

# Sudoku Stuff
from sudoku.getters import get_row, get_group, get_column, has_in_row, has_in_group, has_in_column


class DataMixin:
    data: List[List[int]]
    possibilities: List[List[Union[Tuple[int], int]]]
    size: int
    changed: bool = True
    console: Console = Console(style=Style(bold=True))

    def get_data(self, possibilities: bool = False) -> List[List[int]]:
        return self.possibilities if possibilities else self.data

    def get_possibilities(self) -> List[List[Union[Tuple[int], int]]]:
        return self.possibilities

    def generate_table(self, show_coordinates: bool = False, possibilities: bool = False):
        table = Table(show_header=show_coordinates, header_style="bold red", show_lines=True)
        if show_coordinates:
            for i in range(0 if show_coordinates else 1, self.size + 1):
                table.add_column(str(i) if i > 0 else "X")

        for n, line in enumerate(self.possibilities if possibilities else self.data, start=1):
            row = [str(i) for i in line]
            if show_coordinates:
                row.insert(0, f"[bold red]{n}[/bold red]")
            table.add_row(*row)

        self.console.print(table)

    def print_data(self, show_coordinates: bool = False):
        self.generate_table(show_coordinates=show_coordinates)

    def print_possibilities(self, show_coordinates: bool = False):
        self.generate_table(show_coordinates=show_coordinates, possibilities=True)

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
        return get_row(row_no=row_no, data=self.possibilities if possibilities else self.data)

    def get_column(self, col_no: int, possibilities: bool = False) -> List[int]:
        return get_column(col_no=col_no, data=self.possibilities if possibilities else self.data)

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
    def get_possibilities_counts(numbers: List[Union[Tuple[int], int]]) -> Dict[int, int]:
        counts = defaultdict(lambda: 0)
        for number in numbers:
            if isinstance(number, tuple):
                for n in number:
                    counts[n] += 1

        return counts

    @staticmethod
    def get_number_positions(number: int, numbers: List[Union[Tuple[int], int]]) -> List[int]:
        positions = []
        for cell_no, cell in enumerate(numbers):
            if not isinstance(cell, tuple):
                continue
            if number in cell:
                positions.append(cell_no)

        return positions
