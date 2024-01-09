#! /usr/bin/env python

##########################################################
# GeophoneDisplay.py
#
#   A PyQT5 display that uses a Raspberry Pi that utilizes
#   an ADS1115 breakout board and a SM-24 geophone to 
#   work as a seismograph.
#
#   Created: 12/15/23
#       - Kyle Leleux
#
#   Modified:
#
#   TODO:
#       * Add saving feature
#       * Implement accessibility
#
#   NOTE:
##########################################################

from Geophone import Geophone
from PyQt5.QtWidgets import QApplication, QComboBox, QCheckBox, QVBoxLayout, QHBoxLayout, QLineEdit, QMainWindow, QLabel, QPushButton, QWidget, QSpacerItem, QSizePolicy
from PyQt5 import QtCore, QtWidgets
from Seismograph import Seismograph

class GeophoneDisplay(QMainWindow):

    def __init__(self, mode=1, accessibility=True, parent=None):
        super(GeophoneDisplay, self).__init__(parent)
        self.Seismo = Seismograph()
        self.Geo = Geophone()
        
        # Found a problem with using QMainWindow. It already has its own 
        # layout embedded within, and so we need to create a widget and
        # then add our items to that widget
        self.mode = mode
        self.accessibility = accessibility
        self.setWindowTitle('Seismograph Main Window')
        self.setMinimumSize(725, 500)
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.mainLayout = QVBoxLayout(self.widget)
        
        
        self.setupPlots()
        self.setupControls()

        self.setupStatsTimer()

        #self.setupUI()

    @property
    def accessibility(self) -> bool:
        '''
        The intended use of this display is for an elderly gentleman. As 
        such, I want to add an option that increases the font size and general
        size of the display. I also want to do more research about what it 
        takes to design for accessibility (colorblindness, etc)
        '''
        return self._accessibility

    @accessibility.setter
    def accessibility(self, value:bool):
        self._accessibility = value

    @property
    def mode(self) -> bool:
        '''
        The following modes are available:
            * 0 -> simulated (reading random values)
            * 1 -> running (reading ADS1115 and Geophone)
        '''
        return self._mode

    @mode.setter
    def mode(self, value):
        self._mode = value

    def setupPlots(self):
        self.seismoLayout = QHBoxLayout()
        self.seismoLayout.addWidget(self.Seismo)
        self.mainLayout.addLayout(self.seismoLayout)

    def setupControls(self):
        self.controlsLayout = QHBoxLayout()
        
        horizontalSpacer = QSpacerItem(20, 40, QSizePolicy.Expanding)
        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Expanding)

        # Sample Time Label and LineEdit Setup
        self.sampleTimeLayout = QVBoxLayout()
        self.sampleTimeLabel = QLabel('Sample Time (s):')
        self.sampleTimeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.sampleTimeLineEdit = QLineEdit()
        self.sampleTimeLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.sampleTimeLineEdit.returnPressed.connect(self.sampleTimeChange)

        self.sampleTimeLayout.addWidget(self.sampleTimeLabel)
        self.sampleTimeLayout.addWidget(self.sampleTimeLineEdit)

        # Update Time Label and LineEdit Setup
        self.updateTimeLayout = QVBoxLayout()
        self.updateTimeLabel = QLabel('Update Time (s):')
        self.updateTimeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.updateTimeLineEdit = QLineEdit()
        self.updateTimeLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.updateTimeLineEdit.returnPressed.connect(self.updateTimeChange)
        
        self.updateTimeLayout.addWidget(self.updateTimeLabel)
        self.updateTimeLayout.addWidget(self.updateTimeLineEdit)

        # Samples Per Update
        self.samplesPerUpdateLayout = QVBoxLayout()
        self.samplesPerUpdateLabel = QLabel('Samples Per Update:')
        self.samplesPerUpdateLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.samplesPerUpdateCalc = QLabel()
        self.samplesPerUpdateCalc.setAlignment(QtCore.Qt.AlignCenter)
        
        self.samplesPerUpdateLayout.addWidget(self.samplesPerUpdateLabel)
        self.samplesPerUpdateLayout.addWidget(self.samplesPerUpdateCalc)

        self.totalSamplesLayout = QVBoxLayout()
        self.totalSamplesLabel = QLabel('Total Samples:')
        self.totalSamplesLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.totalSamplesCalc = QLabel()
        self.totalSamplesCalc.setAlignment(QtCore.Qt.AlignCenter)
        
        self.totalSamplesLayout.addWidget(self.totalSamplesLabel)
        self.totalSamplesLayout.addWidget(self.totalSamplesCalc)

        # ADC Gain Label and ComboBox Setup 
        self.gainLayout = QVBoxLayout()
        self.gainLabel = QLabel('ADC Gain:')
        self.gainLabel.setAlignment(QtCore.Qt.AlignCenter)
        if self.mode == 0:
            gains = ['1', '2','3','4','5']
        else:
            gains = list(self.Geo.validGains)
        self.gainCombo = QComboBox()
        #self.gainCombo.addItems(list(self.geo.validGains))
        self.gainCombo.addItems(gains)
        self.gainCombo.currentTextChanged.connect(self.gainChange)
        self.gainLayout.addWidget(self.gainLabel)
        self.gainLayout.addWidget(self.gainCombo)

        # Start/Stop Button Setup
        self.buttonLayout = QVBoxLayout()
        self.startButton = QPushButton('Start/Stop')
        self.startButton.setCheckable(True)
        self.startButton.clicked.connect(self.startChange)

        # Save Button Setup
        self.saveButton = QPushButton('Save Last 24hr')
        self.saveButton.clicked.connect(self.saveChange)
        #self.startLayout.addItem(verticalSpacer)
        self.buttonLayout.addWidget(self.startButton)
        self.buttonLayout.addWidget(self.saveButton)

        # Layout Setup
        self.controlsLayout.addItem(horizontalSpacer)
        self.controlsLayout.addLayout(self.sampleTimeLayout)
        self.controlsLayout.addLayout(self.updateTimeLayout)
        self.controlsLayout.addLayout(self.samplesPerUpdateLayout)
        self.controlsLayout.addLayout(self.totalSamplesLayout)
        self.controlsLayout.addLayout(self.gainLayout)
        self.controlsLayout.addLayout(self.buttonLayout)

        self.mainLayout.addLayout(self.controlsLayout)

    def updateTimeChange(self):
        self.Seismo.updateTime = float(self.updateTimeLineEdit.text())
        self.changeStatsTimerInterval()

    def sampleTimeChange(self):
        self.Seismo.sampleTime = float(self.sampleTimeLineEdit.text())
        self.Seismo.changeTimerInterval()

    def updateSamplesPerUpdate(self):
        self.samplesPerUpdateCalc.setText(str(self.Seismo.samplesPerUpdate))

    def updateTotalSamples(self):
        self.totalSamplesCalc.setText(str(self.Seismo.totalSamples))

    def gainChange(self):
        pass

    def startChange(self):
        if self.Seismo.timer.isActive():
            self.Seismo.timer.stop()
        else:
            self.Seismo.timer.start()

    def saveChange(self):
        pass

    def setupStatsTimer(self):
        self.statsTimer = QtCore.QTimer()
        self.statsTimer.setInterval(self.Seismo.updateTime)
        self.statsTimer.timeout.connect(self.updateStats)
        self.statsTimer.start()

    def changeStatsTimerInterval(self):
        self.statsTimer.stop()
        self.statsTimer.setInterval(self.Seismo.updateTime)
        self.statsTimer.start()

    def updateStats(self):
        self.updateTotalSamples()

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
