from sudoku.simplifications.double import DoublesSimplification


def test_simplify_doubles():
    possibilities = [[(1, 3), (1, 3), (2, 3, 4), (1, 2, 3, 4), (2, 5)]]

    simplifier = DoublesSimplification(
        initial_data=[[0, 0, 0, 0, 0]],
        possibilities=possibilities,
    )

    simplifier.run()

    assert possibilities[0][2] == (2, 4)
    assert possibilities[0][3] == (2, 4)
    assert possibilities[0][4] == (2, 5)
