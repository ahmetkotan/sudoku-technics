from sudoku.technics.base import BaseTechnic


class Singles(BaseTechnic):
    def run(self):
        for row_no, row in enumerate(self.possibilities):
            for col_no, col in enumerate(row):
                if isinstance(col, tuple):
                    if len(col) == 1:
                        self.data[row_no][col_no] = col[0]
                        self.possibilities[row_no][col_no] = col[0]
                        self.fill_possibilities()
