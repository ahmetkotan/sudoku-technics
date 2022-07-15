from sudoku.solver import Sudoku
from sudoku.utils import convert_from_string


string = "906300000300061090050000370000090028001000000000830700000084200694200003000610004"  # hard
data = convert_from_string(string)

u = Sudoku(initial_data=data)
u.solve()
u.print_data(with_rows=True)
u.print_possibilities()
