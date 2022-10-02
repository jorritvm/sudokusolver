from http.client import OK
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtGui import QIntValidator
from gui import Ui_MainWindow


class mainwindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(mainwindow, self).__init__(parent)
        self.setupUi(self)
        self.append_ui()

        self.setup_slots()

    def append_ui(self):
        for box in self.get_boxes():
            box.setInputMask("D")
            # NOTE: because of the inputmask we don't need an int or regex validator anymore
            # digit_validator = QIntValidator(1, 9, self)  # this does not work properly
            # def rx("[1-9]{1}"):
            # digit_validator = QRegularExpressionValidator(rx, self)
            # box.setValidator(digit_validator)

    def setup_slots(self):
        self.action_about.triggered.connect(self.about)

        self.action_wipe.triggered.connect(self.wipe)
        self.btn_wipe.pressed.connect(self.wipe)

        self.action_validate.triggered.connect(self.validate)
        self.btn_validate.pressed.connect(self.validate)

    def about(self):
        QMessageBox.about(
            self,
            "About Sudoku Solver",
            "<h2>Sudoku Solver</h2><p>GPLv3 licensed - 2022<p>Sudoku Solver does what its name says, quickly solve your sudoku.</p><p>Author: Jorrit Vander Mynsbrugge</p>",
        )

    def get_boxes(self):
        x = list()
        for i in range(81):
            x.append(eval("self.t" + str(i)))
        return x

    def get_values(self):
        all_boxes = self.get_boxes()
        return [text_edit.text() for text_edit in all_boxes]  # returns strings

    def wipe(self):
        reply = QMessageBox.question(
            self,
            "Wipe",
            "Are you sure you want to wipe the entire puzzle?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            all_boxes = self.get_boxes()
            for text_edit in all_boxes:
                text_edit.clear()

    def validate(self):
        puzzle = Sudoku(self.get_values())
        if puzzle.is_valid_sudoku():
            QMessageBox.information(
                self,
                "Validation check",
                "Your sudoku puzzle is still valid!",
                QMessageBox.Ok,
            )
        else:
            QMessageBox.critical(
                self,
                "Validation check",
                "Your sudoku puzzle is no longer valid!",
                QMessageBox.Ok,
            )


class Sudoku:
    def __init__(self, values):
        self.values = values
        # self.fix = self.createfix() # de vaste posities ophalen

    def is_valid_sudoku(self):
        """a sudoku puzzle is valid if the same number does not appear twice in a row, a column or a subsquare"""

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
