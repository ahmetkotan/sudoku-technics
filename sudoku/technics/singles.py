# Sudoku Stuff
from sudoku.technics.base import BaseTechnic


class Singles(BaseTechnic):
    def run(self):
        for row_no, row in enumerate(self.possibilities):
            for col_no, col in enumerate(row):
                if isinstance(col, tuple):
                    if len(col) == 1:
                        self.data[row_no][col_no] = col[0]
                        self.possibilities[row_no][col_no] = col[0]
                        self.console.print(
                            f"Found Single Possibility in {row_no + 1}.row " f"{col_no + 1}.column as {col[0]}"
                        )
                        return self.callback()
