from typing import List, Tuple, Union

DATA_TYPE = List[List[Union[Tuple[int], int]]]


def get_group(
    row_no: int,
    col_no: int,
    data: DATA_TYPE,
) -> Union[List[List[int]], List[int]]:
    start_row = row_no - (row_no % 3)
    start_column = col_no - (col_no % 3)
    group_lines = data[start_row : start_row + 3]

    return [line[start_column : start_column + 3] for line in group_lines]


def get_column(col_no: int, data: DATA_TYPE) -> List[int]:
    return [line[col_no] for line in data]


def get_row(row_no: int, data: DATA_TYPE) -> List[int]:
    return data[row_no]


def has_in_column(column: int, number: int, data: DATA_TYPE) -> bool:
    return number in get_column(col_no=column, data=data)


def has_in_group(row_no: int, col_no: int, number: int, data: DATA_TYPE):
    group = get_group(row_no=row_no, col_no=col_no, data=data)
    for line in group:
        if number in line:
            return True

    return False


def has_in_row(row_no: int, number: int, data: DATA_TYPE):
    return number in get_row(row_no=row_no, data=data)


def get_group_positions(row_no: int, col_no: int):
    start_row = row_no - (row_no % 3)
    start_col = col_no - (col_no % 3)
    return [(i, j) for i in range(start_row, start_row + 3) for j in range(start_col, start_col + 3)]
