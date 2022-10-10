"""main file for sudoku solver"""

import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from gui import Ui_MainWindow


class mainwindow(QMainWindow, Ui_MainWindow):
    """UI for the game"""

    def __init__(self, parent=None):
        """constructs and initializes the UI"""
        super(mainwindow, self).__init__(parent)
        self.setupUi(self)
        self.append_ui()

        self.setup_slots()

    def append_ui(self):
        """tweak the UI some more (e.g. input validation)"""
        for box in self.get_boxes():
            box.setInputMask("D")
            # NOTE: because of the inputmask we don't need an int or regex validator anymore
            # digit_validator = QIntValidator(1, 9, self)  # this does not work properly
            # def rx("[1-9]{1}"):
            # digit_validator = QRegularExpressionValidator(rx, self)
            # box.setValidator(digit_validator)

    def setup_slots(self):
        """connects actions and buttons to the corresponding methods"""
        self.action_about.triggered.connect(self.about)

        self.action_generate.triggered.connect(self.generate)

        self.action_wipe.triggered.connect(self.wipe)
        self.btn_wipe.pressed.connect(self.wipe)

        self.action_validate.triggered.connect(self.validate)
        self.btn_validate.pressed.connect(self.validate)

        self.action_hint.triggered.connect(self.hint)
        self.btn_hint.pressed.connect(self.hint)

        self.action_solve.triggered.connect(self.solve)
        self.btn_solve.pressed.connect(self.solve)

    def about(self):
        """displays the about dialog"""
        QMessageBox.about(
            self,
            "About Sudoku Solver",
            """<h2>Sudoku Solver</h2><p>GPLv3 licensed - 2022<p>Sudoku Solver 
            does what its name says, quickly solve your sudoku.</p>
            <p>Author: Jorrit Vander Mynsbrugge</p>""",
        )

    def get_boxes(self):
        """fetches all the qt line edit widgets in a list"""
        x = list()
        for i in range(81):
            x.append(eval("self.t" + str(i)))
        return x

    def get_values(self):
        """fetches all the values (str) from the qt line edit widgets in a list"""
        all_boxes = self.get_boxes()
        return [text_edit.text() for text_edit in all_boxes]  # returns strings

    def draw_sudoku(self, values):
        """draws the values of the sudoku on the gui"""
        boxes = self.get_boxes()
        for i in range(81):
            boxes[i].setText(values[i])

    def generate(self):
        """generate new sudoku puzzle with user confirmation"""
        reply = QMessageBox.question(
            self,
            "Wipe",
            "Are you sure you want to generate a new random puzzle?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.generate_unsafe()

    def generate_unsafe(self):
        """generate new sudoku puzzle without user confirmation"""
        self.wipe_unsafe()

        lines = open("puzzles.txt").read().splitlines()
        random_puzzle = list(random.choice(lines))
        if len(random_puzzle) == 81:
            random_puzzle[:] = [x if x != "0" else "" for x in random_puzzle]
            self.draw_sudoku(random_puzzle)
        else:
            self.generate_unsafe()  # recurse if we find a comment in the txt

    def wipe(self):
        """wipes the puzzle after user confirmation"""
        reply = QMessageBox.question(
            self,
            "Wipe",
            "Are you sure you want to wipe the entire puzzle?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.wipe_unsafe()

    def wipe_unsafe(self):
        """wipes the puzzle without user confirmation"""
        all_boxes = self.get_boxes()
        for box in all_boxes:
            box.clear()

    def validate(self):
        """validates the puzzle and reports to the user"""
        puzzle = Sudoku(self.get_values())
        if puzzle.is_valid_sudoku():
            QMessageBox.information(
                self,
                "Validation check",
                "Your sudoku puzzle is still valid!",
                QMessageBox.Ok,
            )
        else:
            self.show_invalid_message()

    def show_invalid_message(self):
        """shows the user the message their sudoku is invalid"""
        QMessageBox.critical(
            self,
            "Validation check",
            "Your sudoku puzzle is no longer valid!",
            QMessageBox.Ok,
        )

    def hint(self):
        """show the user a hint of the next correct value"""
        puzzle = Sudoku(self.get_values())
        if not puzzle.is_valid_sudoku():
            self.show_invalid_message()
        else:
            idx, value = puzzle.hint()

            if idx >= 0:
                boxes = self.get_boxes()
                boxes[idx].setText(value)

                if puzzle.is_solved_sudoku():
                    self.solved_sudoku_message()
            else:
                self.show_no_hint_message()

    def show_no_hint_message(self):
        """shows the user the message there are no straightforward hints"""
        QMessageBox.critical(
            self,
            "Hint",
            "Your next sudoku move is not a clear call. Make a guess and go on.",
            QMessageBox.Ok,
        )

    def solve(self):
        """completes the puzzle automatically"""
        puzzle = Sudoku(self.get_values())
        if not puzzle.is_valid_sudoku():
            self.show_invalid_message()
        else:
            success = puzzle.solve()
            if success:
                self.draw_sudoku(puzzle.values)
                self.solved_sudoku_message()
            else:
                self.unsolved_sudoku_message()

    def solved_sudoku_message(self):
        """informs the user the puzzle is solved"""
        QMessageBox.information(
            self,
            "Sudoku solved",
            "Your sudoku puzzle is solved!",
            QMessageBox.Ok,
        )

    def unsolved_sudoku_message(self):
        """informs the user the puzzle can't be solved"""
        QMessageBox.critical(
            self,
            "Sudoku NOT solved",
            "Your sudoku puzzle is too difficult for me to solve!",
            QMessageBox.Ok,
        )


class Sudoku:
    """this class represents the game & game functionality"""

    def __init__(self, values):
        self.values = values

    def position_to_identifiers(self, i_pos):
        """given a position in the puzzle, returns the row, column
        and square identifier"""
        i_row = int(i_pos / 9)
        i_col = int(i_pos % 9)
        i_sq = int(i_pos % 9 / 3) + 3 * int((i_pos / 27))  # magic maths
        return (i_row, i_col, i_sq)

    def get_row(self, i, n=9):
        """returns first n values of row with index i"""
        return self.values[i * 9 : i * 9 + n]

    def get_column(self, i, n=9):
        """returns first n values of column with index i"""
        x = list()
        p = 0
        for value in self.values[0 : n * 9]:
            if p % 9 == i:
                x.append(value)
            p += 1
        return x

    def get_square(self, i, n=9):
        """returns first n values of square with index i"""
        if i < 3:
            start = i * 3
        elif 3 <= i < 6:
            start = (i - 3) * 3 + 27
        elif 6 <= i < 9:
            start = (i - 6) * 3 + 54
        x = list()
        for u in range(3):
            offset = start + u * 9
            for p in range(3):
                x.append(self.values[offset + p])
        return x[:n]

    def is_valid_sudoku(self):
        """a sudoku puzzle is valid if the same number does not appear
        twice in a row, a column or a subsquare"""
        valid = True
        for i_row in range(9):
            valid = valid and self.is_valid_nine(self.get_row(i_row))
        for i_col in range(9):
            valid = valid and self.is_valid_nine(self.get_column(i_col))
        for i_sq in range(9):
            valid = valid and self.is_valid_nine(self.get_square(i_sq))
        return valid

    def is_valid_nine(self, subset):
        """a set of nine is valid if each number only appears once"""
        subset = [x for x in subset if x]  # keep non empty values
        uniques = set(subset)  # make them unique
        return len(subset) == len(uniques)

    def determine_possibilities(self):
        """creates a list where every element contains a list of possible
        values for that position,
        returns False if some fields have no more possibilities"""
        possibilities = list()

        for i_pos in range(81):
            if self.values[i_pos]:
                # when the value is already filled in the only possibility is that value
                # possibilities.append([self.values[i_pos]])
                possibilities.append([])
            else:
                # all values that are not in the R, C or S are possible
                i_row, i_col, i_sq = self.position_to_identifiers(i_pos)

                pbx = [str(x) for x in range(1, 10)]
                row = self.get_row(i_row)
                col = self.get_column(i_col)
                square = self.get_square(i_sq)

                pbx = [elem for elem in pbx if elem not in row]
                pbx = [elem for elem in pbx if elem not in col]
                pbx = [elem for elem in pbx if elem not in square]

                if len(pbx) == 0:
                    return False

                possibilities.append(pbx)
        return possibilities

    def hint(self):
        """returns the first possible position + value that can be filled in"""
        possibilities = self.determine_possibilities()
        could_not_find_a_hint = True
        for idx, possibility in enumerate(possibilities):
            if len(possibility) == 1:
                could_not_find_a_hint = False
                self.values[idx] = possibility[0]
                # print((idx, possibility[0]))
                return (idx, possibility[0])
        if could_not_find_a_hint:
            return (-1, -1)

    def is_solved_sudoku(self):
        """a solved sudoku is a valid sudoku with 81 values filled in"""
        if self.is_valid_sudoku():
            subset = [x for x in self.values if x]  # keep non empty values
            if len(subset) == 81:
                return True
        return False

    def solve(self, i = 0):
        """a sudoku is solved by looking for remaining possible values per
        field. if one possibility remains, this value is safely filled in.
        if only cells of 2 or more possibilities remain, a 'guess' must first
        be made to proceed, when such a guess is made, the sudoku can be 'bust' 
        in which case we return False
        
        return true if solve was successfull, false otherwise"""
        pre_solve_values = self.values[:] # copy by value

        while not self.is_solved_sudoku():
            possibilities = self.determine_possibilities()
            
            # if the sudoku is bust return False
            if not possibilities:
                return False
          
            # verify all possibilities
            need_branch = True
            for idx, possibility in enumerate(possibilities):
                # if only one possibility exists: always fill it out
                if len(possibility) == 1:
                    self.values[idx] = possibility[0]
                    need_branch = False
            
            # sometimes the sudoku is too hard and we could not fill out 
            # a single value (all boxes have more than 1 possibility)
            # we now need to make a choice 
            if need_branch:
                # look for the smallest group of possibilities > 1
                group_size = 10
                for idx, possibility in enumerate(possibilities):
                    if 1 < len(possibility) < group_size:
                        group_size = len(possibility)
                        branch_id = idx
                        branch_possibilities = possibility

                # branch and go depth first
                branch_values = self.values[:]
                for branch_possibility in branch_possibilities:
                    branch_values[branch_id] = branch_possibility
                    puzzle_branch = Sudoku(branch_values[:])
                    success = puzzle_branch.solve()
                    if success and puzzle_branch.is_solved_sudoku():
                        self.values = puzzle_branch.values
                        break
                    else:
                        pass
                        # print("bust branch")

        # return success bool
        if not self.is_solved_sudoku():
            self.values = pre_solve_values
            return False
        else:
            return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwidget = mainwindow()
    mainwidget.show()
    sys.exit(app.exec_())
