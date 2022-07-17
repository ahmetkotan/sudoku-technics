# Standard Library
from copy import deepcopy

# Sudoku Stuff
from sudoku.simplifications.sky_scraper import SkyScraperSimplification

column_possibilities = [
    [0] * 9,
    [0] * 9,
    [0, 0, 0, (1, 3, 5, 6), 0, 0, (2, 6), 0, 0],  # 4th and 7th
    [0, 0, 0, (3, 6), 0, 0, 0, (2, 6), 0],  # 4th and 8th
    [0] * 9,
    [0, 0, 0, 0, 0, 0, (3, 6), 0, 0],  # 7th
    [0] * 9,
    [0] * 9,
    [0] * 9,
]

row_possibilities = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, (1, 3, 5, 6), 0, 0, (3, 6), 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, (2, 6), 0, 0],
    [0, 0, 0, (2, 6), 0, 0, 0, (3, 6), 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]


def test_find_intersection_positions():
    first_point = (3, 3)
    second_point = (5, 6)
    expected_points = [(2, 3), (2, 6)]

    simplifier = SkyScraperSimplification(
        initial_data=[], possibilities=column_possibilities
    )
    positions = simplifier.find_intersection_positions(
        first_point=first_point,
        second_point=second_point,
        expected_points=expected_points,
    )
    assert len(positions) == 1
    assert positions[0] == (3, 7)


def test_simplify_column():
    possibilities = deepcopy(column_possibilities)
    simplifier = SkyScraperSimplification(initial_data=[], possibilities=possibilities)
    simplifier.simplify_column(col_no=3)

    assert possibilities[2][3] == (1, 3, 5, 6)
    assert possibilities[2][6] == (2, 6)
    assert possibilities[3][7] == tuple([2])
    assert possibilities[5][6] == (3, 6)


def test_simplify_row():
    possibilities = deepcopy(row_possibilities)
    simplifier = SkyScraperSimplification(initial_data=[], possibilities=possibilities)
    simplifier.simplify_row(row_no=2)

    assert possibilities[2][3] == (1, 3, 5, 6)
    assert possibilities[2][6] == (3, 6)
    assert possibilities[4][6] == tuple([2])
    assert possibilities[5][3] == (2, 6)
    assert possibilities[5][7] == (3, 6)
