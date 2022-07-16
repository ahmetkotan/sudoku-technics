from sudoku.simplifications.double import DoublesSimplification


def test_simplify_rows():
    possibilities = [[(1, 3), (1, 3), (2, 3, 4), (1, 2, 3, 4), (2, 5)]]

    simplifier = DoublesSimplification(
        initial_data=[[0, 0, 0, 0, 0]],
        possibilities=possibilities,
        callback=lambda: None,
    )

    simplifier.simplify_row(row_no=0)

    assert possibilities[0][2] == (2, 4)
    assert possibilities[0][3] == (2, 4)
    assert possibilities[0][4] == (2, 5)


def test_simplify_columns():
    possibilities = [[(1, 3)], [(1, 3)], [(2, 3, 4)], [(1, 2, 3, 4)], [(2, 5)]]

    simplifier = DoublesSimplification(
        initial_data=[[0], [0], [0], [0], [0]],
        possibilities=possibilities,
        callback=lambda: None,
    )

    simplifier.simplify_column(col_no=0)

    assert possibilities[2][0] == (2, 4)
    assert possibilities[3][0] == (2, 4)
    assert possibilities[4][0] == (2, 5)
