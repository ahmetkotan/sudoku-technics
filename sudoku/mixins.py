from typing import List, Tuple, Union


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
        return number in self.data[row]

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
        return self.find_in_column(column=column, number=number) != -1

    def get_row(self, row_no: int, possibilities: bool = False) -> List[int]:
        return self.possibilities[row_no] if possibilities else self.data[row_no]

    def get_column(self, col_no: int, possibilities: bool = False) -> List[int]:
        return [
            line[col_no]
            for line in (self.possibilities if possibilities else self.data)
        ]

    def get_group(
        self, row_no: int, col_no: int, possibilities: bool = False, as_list: bool = False
    ) -> Union[List[List[int]], List[int]]:
        start_row = row_no - (row_no % 3)
        start_column = col_no - (col_no % 3)
        group_lines = (
            self.possibilities[start_row: start_row + 3]
            if possibilities
            else self.data[start_row: start_row + 3]
        )

        if as_list:
            group: List[int] = []
            for line in group_lines:
                group.extend(line[start_column: start_column + 3])
            return group

        return [line[start_column: start_column + 3] for line in group_lines]

    def has_in_group(self, row_no: int, col_no: int, number: int) -> bool:
        for line in self.get_group(row_no=row_no, col_no=col_no):
            if number in line:
                return True

        return False

    def fill_possibilities(self):
        self.changed = False
        for row_no, line in enumerate(self.data):
            line_possibilities = set(range(0, self.size + 1)) - set(line)
            for col_no in range(self.size):
                if line[col_no] != 0:
                    continue

                possibilities = [
                    number
                    for number in line_possibilities
                    if not self.has_in_column(column=col_no, number=number)
                       and not self.has_in_group(
                        row_no=row_no, col_no=col_no, number=number
                    )
                ]
                if len(possibilities) == 0:
                    self.print_possibilities()
                    raise Exception(f"Error in {row_no + 1}.row {col_no + 1}.column")
                elif len(possibilities) == 1:
                    print(
                        f"Found one possibility. Changed {row_no + 1}.row {col_no + 1}.columns with {possibilities[0]}"
                    )
                    self.data[row_no][col_no] = possibilities[0]
                    self.possibilities[row_no][col_no] = possibilities[0]
                    self.changed = True
                else:
                    self.possibilities[row_no][col_no] = tuple(possibilities)

    def reload_possibilities(self):
        self.fill_possibilities()
        while self.changed:
            self.fill_possibilities()
