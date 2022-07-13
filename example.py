from sudoku.solver import Sudoku
from sudoku.utils import convert_from_string


string = "605740000704602058200000670020405780000000526000076030568090040040067095097500060"  # easy
data = convert_from_string(string)

u = Sudoku(initial_data=data)
u.solve()
u.print_data()
