import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import *
from PyQt5.QtGui import *


from game import *


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwidget = mainwindow()
    mainwidget.show()
    sys.exit(app.exec_())
