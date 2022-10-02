from sudoku_solver import Sudoku


def test_position_to_identifiers():
    val = [""] * 81
    val[0:9] = ["1", "2", "3", "4", "5", "6", "7", "8", ""]

    puzzle = Sudoku(val)
    assert puzzle.position_to_identifiers(0) == (0, 0, 0)
    assert puzzle.position_to_identifiers(1) == (0, 1, 0)
    assert puzzle.position_to_identifiers(8) == (0, 8, 2)
    assert puzzle.position_to_identifiers(60) == (6, 6, 8)
