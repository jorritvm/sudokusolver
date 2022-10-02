from PyQt5.QtWidgets import QMainWindow
from gui import Ui_MainWindow


class mainwindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(mainwindow, self).__init__(parent)
        self.setupUi(self)
        # self.t = self.getwidgetlist()

        # slots
        # self.setupslots()
