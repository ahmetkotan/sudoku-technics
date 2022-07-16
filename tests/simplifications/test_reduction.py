from sudoku.simplifications.reduction import ReductionSimplification
from typing import List, Union, Tuple


def test_simplify_rows():
    possibilities = [
        [0] * 9,
        [0] * 9,
        [0] * 9,
        [(3, 7, 9), 4, (3, 5, 7, 9), 8, (2, 3, 6, 7), (5, 7), 1, (2, 3, 6, 7, 9), (2, 3, 5, 9)],
        [6, (1, 3, 5, 8), 2, (1, 3, 5), (1, 3, 7), 4, (5, 7), (3, 7, 8, 9), (3, 5, 8, 9)],
        [(3, 7, 8), (1, 3, 5, 8), (1, 3, 5, 7, 8), (1, 3, 5, 6), (1, 2, 3, 6, 7), 9, (2, 6), (2, 3, 6, 7, 8), 4],
        [0] * 9,
        [0] * 9,
        [0] * 9,
    ]

    simplifier = ReductionSimplification(
        initial_data=[
            [0] * 9,
            [0] * 9,
            [0] * 9,
            [0, 4, 0, 8, 0, 0, 1, 0, 0],
            [6, 0, 2, 0, 0, 4, 0, 0, 0],
            [0, 0, 0, 0, 0, 9, 0, 0, 4],
            [0] * 9,
            [0] * 9,
            [0] * 9,
        ],
        possibilities=possibilities,
        size=9,
        callback=lambda: None
    )

    simplifier.simplify()

    assert possibilities[3][7] == (2, 3, 6, 7)
    assert possibilities[3][8] == (2, 3, 5)
    assert possibilities[4][7] == (3, 7, 8, 9)


def test_simplify_columns():
    possibilities: List[List[Union[Tuple[int, ...], int]]] = [
        [0] * 3 + [(3, 7, 9), 6, (3, 7, 8)] + [0] * 3,
        [0] * 3 + [4, (1, 3, 5, 8), (1, 3, 5, 8)] + [0] * 3,
        [0] * 3 + [(3, 5, 7, 9), 2, (1, 3, 5, 7, 8)] + [0] * 3,
        [0] * 3 + [8, (1, 3, 5), (1, 3, 5, 6)] + [0] * 3,
        [0] * 3 + [(2, 3, 6, 7), (1, 3, 7), (1, 2, 3, 6, 7)] + [0] * 3,
        [0] * 3 + [(5, 7), 4, 9] + [0] * 3,
        [0] * 3 + [1, (5, 7), (2, 6)] + [0] * 3,
        [0] * 3 + [(2, 3, 6, 7, 9), (3, 7, 8, 9), (2, 3, 6, 7, 8)] + [0] * 3,
        [0] * 3 + [(2, 3, 5, 9), (3, 5, 8, 9), 4] + [0] * 3
    ]
    simplifier = ReductionSimplification(initial_data=[], possibilities=possibilities)

    simplifier.simplify()

    assert possibilities[7][3] == (2, 3, 6, 7)
    assert possibilities[8][3] == (2, 3, 5)
    assert possibilities[7][4] == (3, 7, 8, 9)

