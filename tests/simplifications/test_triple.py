# Sudoku Stuff
from sudoku.simplifications.triple import TripleSimplification


def test_simplify_rows():
    possibilities = [[(1, 5), (1, 8), (1, 5, 8), (3, 5, 9), (1, 3, 5, 9)]]

    simplifier = TripleSimplification(
        initial_data=[[0, 0, 0, 0, 0]],
        possibilities=possibilities,
        callback=lambda: None,
    )
    simplifier.simplify_row(row_no=0)

    assert possibilities[0][0] == (1, 5)
    assert possibilities[0][1] == (1, 8)
    assert possibilities[0][2] == (1, 5, 8)
    assert possibilities[0][3] == (3, 9)
    assert possibilities[0][4] == (3, 9)
