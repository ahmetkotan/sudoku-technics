from sudoku.getters import get_group_positions


def test_get_group_positions():
    positions = get_group_positions(row_no=5, col_no=6)

    assert len(positions) == 9
    assert positions[0] == (3, 6)
    assert positions[3] == (4, 6)
    assert positions[4] == (4, 7)
    assert positions[8] == (5, 8)
