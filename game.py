from PyQt5.QtWidgets import QMainWindow, QMessageBox
from gui import Ui_MainWindow


class mainwindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(mainwindow, self).__init__(parent)
        self.setupUi(self)

        self.all_boxes = self.get_boxes()
        self.setupslots()

    def setupslots(self):
        self.action_about.triggered.connect(self.about)
        self.action_wipe.triggered.connect(self.wipe)
        self.btn_wipe.pressed.connect(self.wipe)

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

    def wipe(self):
        for text_edit in self.all_boxes:
            text_edit.clear()

        # QObject.connect(self.actionEmpty_puzzle,SIGNAL("triggered(bool)"),self.emptypuzzle)
        # QObject.connect(self.actionAbout_Sudokusolver,SIGNAL("triggered(bool)"),self.showabout)
        # QObject.connect(self.pushButton,SIGNAL("clicked(bool)"),self.solvethissudoku)
