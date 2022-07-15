from sudoku.solver import Sudoku
from sudoku.utils import convert_from_string


string = "204000000000004591010506002070000000100000850000091070045000007006800004000030020"  # hard
data = convert_from_string(string)

u = Sudoku(initial_data=data)
u.solve()
u.print_data(with_rows=True)
u.print_possibilities()
