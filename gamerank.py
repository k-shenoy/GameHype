import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic


qtCreatorFile = "mainwindow.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.mlButton.clicked.connect(self.calculate_gamerank)
    def calculate_gamerank(self):
        team1 = self.team1.text()
        team2 = self.team2.text()
        nba = ""
        if self.rbNBA.isChecked():
            nba = self.comboBox.currentText()
        self.results_output.setText(nba)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
