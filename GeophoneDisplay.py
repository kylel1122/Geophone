#import Geophone
from PyQt5.QtWidgets import QApplication, QComboBox, QCheckBox, QVBoxLayout, QHBoxLayout, QLineEdit, QMainWindow, QLabel, QPushButton, QWidget, QSpacerItem, QSizePolicy
from PyQt5 import QtCore, QtWidgets
from Seismograph import Seismograph

class GeophoneDisplay(QMainWindow):

    def __init__(self, accessibility = True, parent=None):
        super(GeophoneDisplay, self).__init__(parent)
        self.Seismo = Seismograph()
        #self.geo = Geophone()
        
        # Found a problem with using QMainWindow. It already has its own 
        # layout embedded within, and so we need to create a widget and
        # then add our items to that widget

        self._accessibility = accessibility
        self.setWindowTitle('Seismograph Main Window')
        self.setMinimumSize(725, 500)
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.mainLayout = QVBoxLayout(self.widget)
        #self.mainLayout = QVBoxLayout()
        #self.setLayout(self.mainLayout)
        
        
        self.setupPlots()
        self.setupControls()

        #self.setupUI()

    def setupPlots(self):
        self.seismoLayout = QHBoxLayout()
        self.seismoLayout.addWidget(self.Seismo)
        self.mainLayout.addLayout(self.seismoLayout)

    def setupControls(self):
        self.controlsLayout = QHBoxLayout()
        
        horizontalSpacer = QSpacerItem(20, 40, QSizePolicy.Expanding)

        self.sampleTimeLayout = QVBoxLayout()
        self.sampleTimeLabel = QLabel('Sample Time (s)')
        self.sampleTimeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.sampleTimeLineEdit = QLineEdit()
        #self.sampleTimeLineEdit.returnPressed.connect(self.sampleTimeChange)

        self.sampleTimeLayout.addWidget(self.sampleTimeLabel)
        self.sampleTimeLayout.addWidget(self.sampleTimeLineEdit)

        self.updateTimeLayout = QVBoxLayout()
        self.updateTimeLabel = QLabel('Update Time (s)')
        self.updateTimeLineEdit = QLineEdit()
        #self.updateTimeLineEdit.returnPressed.connect(self.updateTimeChanged)
        
        self.updateTimeLayout.addWidget(self.updateTimeLabel)
        self.updateTimeLayout.addWidget(self.updateTimeLineEdit)

        self.gainLayout = QVBoxLayout()
        self.gainLabel = QLabel('ADC Gain:')
        self.gainLabel.setAlignment(QtCore.Qt.AlignCenter)
        test_gains = ['1', '2','3','4','5']
        self.gainCombo = QComboBox()
        #self.gainCombo.addItems(list(self.geo.validGains))
        self.gainCombo.addItems(test_gains)
        #self.gainCombo.currentTextChanged.connect(self.gainChange)
        self.gainLayout.addWidget(self.gainLabel)
        self.gainLayout.addWidget(self.gainCombo)

        self.controlsLayout.addItem(horizontalSpacer)
        self.controlsLayout.addLayout(self.sampleTimeLayout)
        self.controlsLayout.addLayout(self.updateTimeLayout)
        self.controlsLayout.addLayout(self.gainLayout)

        self.mainLayout.addLayout(self.controlsLayout)

    def setupUI(self):
        #TODO: Right now, i have a lot of potential widgets, but with 
        #      no idea on how I should lay them out. Figure that out.
        self.setWindowTitle('Seismograph Main Window')

        self.layout = QGridLayout()

        # Setting up some widgets I think I will need without much else thought for right now
        
        self.gainCombo = QComboBox()
        self.setLayout(layout)

        # TODO: Need to do something with this value once it is set
        self.gainCombo.addItems(list(self.geo.validGains))
        self.gainCombo.currentTextChanged.connect(self.gainChange)
        
        self.readingLabel = QLabel()
        
        self.sampleTime = QLineEdit()
        self.sampleTime.returnPressed.connect(self.sampleTimeChange)

        self.sampleTimeRBV = QLabel()
        
        layout.addWidget(self.readingLabel, 0, 0, 2)
        layout.addWidget(self.sampleTime, 1, 0)
        layout.addWidget(self.sampleTimeRBV, 1, 1)


        

        self.startBtn = QPushButton()


        self.saveLast24Btn = QPushButton()
        # TODO: Move these to pyqt graph widget probably
        self.zoomInBtn = QPushButton()
        self.zoomOutBtn = QPushButton()
        self.resetWindowBtn = QPushButton()
        
        self.show()
    
    def ui_filepath(self):
        return None

        # TODO: slider to see back throughout the day or zoom in and out
'''
    def gainChange(self):
        self.geo.gain(int(self.gainCombo.currentText()))

    def sampleTimeChange(self):
        self.geo.sampleTime(float(self.sampleTime.currentText()))
        '''
        


app = QtWidgets.QApplication([])
main = GeophoneDisplay()
main.show()
app.exec()
