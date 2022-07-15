from sudoku.solver import Sudoku
from sudoku.utils import convert_from_string


string = "009586000000020000400000683900650032060700098030200704003000000620015040000400050"  # medium
data = convert_from_string(string)

u = Sudoku(initial_data=data)
u.solve()
u.print_data()
