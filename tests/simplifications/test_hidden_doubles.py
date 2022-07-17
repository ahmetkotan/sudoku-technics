# Sudoku Stuff
from sudoku.simplifications.hidden_double import HiddenDoubleSimplification


def test_simplify_row():
    possibilities = [
        [
            5,
            (2, 3, 6, 8),
            4,
            9,
            (1, 2, 3, 6, 7, 8),
            (1, 2, 7, 8),
            (2, 3, 6),
            (2, 3, 6, 8),
            (2, 3, 8),
        ]
    ]

    simplifier = HiddenDoubleSimplification(
        initial_data=[[0, 0, 0, 0, 0, 0, 0, 0, 0]], possibilities=possibilities, callback=lambda: None,
    )
    simplifier.simplify_row(row_no=0)

    assert possibilities[0][0] == 5
    assert possibilities[0][1] == (2, 3, 6, 8)
    assert possibilities[0][2] == 4
    assert possibilities[0][3] == 9
    assert possibilities[0][4] == (1, 7)
    assert possibilities[0][5] == (1, 7)
    assert possibilities[0][6] == (2, 3, 6)
    assert possibilities[0][7] == (2, 3, 6, 8)
    assert possibilities[0][8] == (2, 3, 8)

