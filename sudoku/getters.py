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


def has_in_column(column: int, number: int, data: List[List[int]]) -> bool:
    data = get_column(col_no=column, data=data)
    return number in data


def has_in_group(row_no: int, col_no: int, number: int, data: DATA_TYPE):
    group = get_group(row_no=row_no, col_no=col_no, data=data)
    for line in group:
        if number in line:
            return True

    return False
