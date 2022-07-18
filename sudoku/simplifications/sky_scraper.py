# Standard Library
from typing import List, Tuple, Callable, Generator

# Sudoku Stuff
from sudoku.getters import get_group_positions
from sudoku.simplifications.base import BaseSimplifier


class SkyScraperSimplification(BaseSimplifier):
    def find_intersection_positions(
        self,
        first_point: Tuple[int, int],
        second_point: Tuple[int, int],
        expected_points: List[Tuple[int, int]],
    ) -> List[Tuple[int, int]]:
        first_x, first_y = first_point
        first_effected_points = (
            [(first_x, i) for i in range(self.size) if i != first_y]
            + [(i, first_y) for i in range(self.size) if i != first_x]
            + get_group_positions(row_no=first_x, col_no=first_y)
        )
        second_x, second_y = second_point
        second_effected_points = (
            [(second_x, i) for i in range(self.size) if i != second_y]
            + [(i, second_y) for i in range(self.size) if i != second_x]
            + get_group_positions(row_no=second_x, col_no=second_y)
        )
        intersection_positions = set(first_effected_points).intersection(second_effected_points) - set(expected_points)
        return [(x, y) for x, y in intersection_positions if isinstance(self.possibilities[x][y], tuple)]

    def find_intersection_points(
        self, actual_no: int, get_function: Callable
    ) -> Generator[Tuple[int, int, int, int, int], None, None]:
        numbers = get_function(actual_no, possibilities=True)
        counts = self.get_possibilities_counts(numbers=numbers)
        for pair in [key for key, value in counts.items() if value == 2]:
            for tmp_no in range(self.size):
                if tmp_no == actual_no or int(actual_no / 3) == int(tmp_no / 3):
                    continue
                tmp_numbers = get_function(tmp_no, possibilities=True)
                tmp_counts = self.get_possibilities_counts(numbers=tmp_numbers)
                if pair in [key for key, value in tmp_counts.items() if value == 2]:
                    pair_positions = self.get_number_positions(number=pair, numbers=numbers)  # column numbers
                    tmp_positions = self.get_number_positions(number=pair, numbers=tmp_numbers)  # column numbers
                    if pair_positions[0] == tmp_positions[0]:
                        intersection_point = pair_positions[0]
                    elif pair_positions[1] == tmp_positions[1]:
                        intersection_point = pair_positions[1]
                    else:
                        continue

                    first_disc_point = (set(pair_positions) - {intersection_point}).pop()
                    second_disc_point = (set(tmp_positions) - {intersection_point}).pop()
                    if first_disc_point == second_disc_point:
                        continue
                    yield pair, first_disc_point, second_disc_point, intersection_point, tmp_no

    def get_effected_points(
        self,
        first_row: int,
        first_col: int,
        second_row: int,
        second_col: int,
        intersection_point: int,
        pair: int,
    ) -> Generator[Tuple[int, int, Tuple[int, ...]], None, None]:
        first_point = (first_row, first_col)
        second_point = (second_row, second_col)
        expected_points = [
            (first_row, intersection_point),
            (second_row, intersection_point),
        ]
        for (effected_row, effected_col) in self.find_intersection_positions(
            first_point=first_point,
            second_point=second_point,
            expected_points=expected_points,
        ):
            cell = self.possibilities[effected_row][effected_col]
            if pair in cell and len(cell) > 1:
                self.possibilities[effected_row][effected_col] = tuple(sorted(set(cell) - {pair}))
                self.changed = True
                yield effected_row, effected_col, cell

    def simplify_row(self, row_no: int):
        for (
            pair,
            first_disc_column,
            second_disc_column,
            intersection_point,
            tmp_row,
        ) in self.find_intersection_points(actual_no=row_no, get_function=self.get_row):
            for (effected_row, effected_col, cell) in self.get_effected_points(
                first_row=row_no,
                first_col=first_disc_column,
                second_row=tmp_row,
                second_col=second_disc_column,
                intersection_point=intersection_point,
                pair=pair,
            ):
                self.console.print(
                    f"Simplified Skyscraper Row {effected_row + 1}.row {effected_col + 1}.column with "
                    f"{pair}. Old: {cell}"
                )

    def simplify_column(self, col_no: int):
        for (
            pair,
            first_disc_row,
            second_disc_row,
            intersection_point,
            tmp_col,
        ) in self.find_intersection_points(actual_no=col_no, get_function=self.get_column):
            for (effected_row, effected_col, cell) in self.get_effected_points(
                first_row=first_disc_row,
                first_col=col_no,
                second_row=second_disc_row,
                second_col=tmp_col,
                intersection_point=intersection_point,
                pair=pair,
            ):
                self.console.print(
                    f"Simplified Skyscraper Column {effected_row + 1}.row {effected_col + 1}.column with "
                    f"{pair}. Old: {cell}"
                )

    def simplify_group(self, group_no: int):
        pass
