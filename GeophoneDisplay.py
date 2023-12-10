from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5 import QtWidgets

class GeophoneDisplay(QMainWindow):

    def __init__(self):
        super(GeophoneDisplay, self).__init__()


        self.setGeometry(200, 200, 300, 300)

        self.setupUI()

    def setupUI(self):
        self.setWindowTitle('Seismograph Main Window')
        self.createGridLayout()
