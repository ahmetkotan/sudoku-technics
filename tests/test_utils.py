from sudoku.utils import convert_from_string


def test_convert_from_string():
    data = convert_from_string("605740000704", size=3)  # 12 digit
    assert len(data) == 4
    assert data[0] == [6, 0, 5]

