# Sudoku Stuff
from sudoku.solver import Sudoku
from sudoku.utils import convert_from_string

string = "040800100602000000000009000190050407000400010500000000000096800000003006270000040"  # expert
data = convert_from_string(string)

u = Sudoku(initial_data=data)
u.solve()
u.print_data()
u.print_possibilities()
