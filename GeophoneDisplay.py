import Geophone
from PyQt5.QtWidgets import QApplication, QComboBox, QCheckBox, QLineEdit QMainWindow, QLabel, QPushButton
from PyQt5 import QtWidgets
import Seismograph

class GeophoneDisplay(QMainWindow):

    def __init__(self, accessibility = True):
        super(GeophoneDisplay, self).__init__()
        self.geo = Geophone()
        
        self.accessibility = accessibility
        
        self.setGeometry(200, 200, 300, 300)

        self.setupUI()

    def setupUI(self):
        self.setWindowTitle('Seismograph Main Window')
        self.createGridLayout()

        # Setting up some widgets I think I will need without much else thought for right now
        self.gainCombo = QComboBox()
        # TODO: Need to do something with this value once it is set
        self.gainCombo.addItems(list(self.geo.validGains))
        self.gainCombo.currentTextChanged.connect(self.gainChange)

        self.readingLabel = QLabel()
        
        self.sampleTime = QLineEdit()
        self.sampleTime.returnPressed.connect(self.sampleTimeChange)

        self.sampleTimeRBV = QLabel()
        
        self.startBtn = QPushButton()


        self.saveLast24Btn = QPushButton()
        # TODO: Move these to pyqt graph widget probably
        self.zoomInBtn = QPushButton()
        self.zoomOutBtn = QPushButton()
        self.resetWindowBtn = QPushButton()
        

        # TODO: slider to see back throughout the day or zoom in and out

    def gainChange(self):
        self.geo.gain(int(self.gainCombo.currentText()))

    def sampleTimeChange(self):
        self.geo.sampleTime(float(self.sampleTime.currentText()))
