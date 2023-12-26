#! /usr/bin/env python

##########################################################
# Seismograph.py
#
#   A pyqtgraph object used to display voltage readings
#
#   Created: 12/10/23
#       - Kyle Leleux
#
#   Modified:
#
#   TODO:
#
#   NOTE:
#          
##########################################################

import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets
from random import randint
import time
#import Geophone


class Seismograph(pg.PlotWidget):
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')

    def __init__(self, update_time=2, parent=None):
        super(Seismograph, self).__init__(parent)
        self.updateTime = update_time
        self.sampleTime = 0.1 #ms
        self.time = []
        self.response = []
        self.timeBuffer = []
        self.responseBuffer = []
        self.setupPlot()
        self.setupTimer()

        self.secondsInDay = 60 * 60 * 24


    def setupPlot(self):
        units = 'mV'
        gain = 50
        self.seismo = self.getPlotItem()
        #self.setCentralWidget(self.seismo)
        #self.seismo.setBackground('w')
        pen = pg.mkPen(color=(255, 0, 0))

        self.seismo.setTitle(f'Response ({units}) Vs Time', color='b', size='20pt')
        styles = {'color':'red', 'font-size':'18px'}
        self.seismo.setLabel('left', f'Response ({units})', **styles)
        self.seismo.setLabel('bottom', f'Time (s)', **styles)
        self.seismo.addLegend()
        self.seismo.showGrid(x=True, y=True)
        self.seismo.setYRange(gain, -1*gain)

        self.line = self.seismo.plot(self.time,
                                     self.response,
                                     name='Response',
                                     pen=pen,
                                     )



    @property
    def updateTime(self) -> int:
        return self._updateTime

    @updateTime.setter
    def updateTime(self, value:float):
        '''
        Convert to milliseconds because Qt.Timer expects milliseconds
        '''
        self._updateTime = value * 1000

    @property
    def sampleTime(self) -> int:
        return self._sampleTime

    @sampleTime.setter
    def sampleTime(self, value:float):
        '''
        Convert to milliseconds because Qt.Timer expects milliseconds
        '''
        self._sampleTime = value * 1000

    @property
    def samplesPerUpdate(self) -> int:
        return (self.updateTime / self.sampleTime)

    @property
    def totalSamples(self):
        return len(self.time)

    def updatePlot(self):
        # My thoughts here are:
        # We should update the plots at a regular frequency, but maybe not at the
        # read frequency of the sample time. so something like (updateTime/sampleTime)
        # points of data

        # Move buffer up by sampled data points
        # What does a full day of samples look like. should we start scrolling??
        '''
        if len(timePlot) < fullDay:
            self.timePlot.append(self.timeBuffer)
            self.seisPlot.append(self.seisBuffer)
        else:
            self.timePlot = self.timePlot[self.updateLength:] 
            self.timePlot.append(self.timeBuffer)
            self.seisPlot = self.seisPlot[self.updateLength:]
            self.seisPlot.append(self.seisBuffer)
        '''
        self.timeBuffer.append(time.time())
        self.responseBuffer.append(randint(20,40))
        
        if len(self.responseBuffer) >= (self.updateTime/self.sampleTime):
            if len(self.time) < self.secondsInDay:
                self.time = self.time + self.timeBuffer
                self.response = self.response + self.responseBuffer
            else:
                self.time = self.time[len(self.timeBuffer):]
                self.time = self.time + self.timeBuffer
                self.response = self.response[len(self.responseBuffer):]
                self.response = self.response + self.responseBuffer

            self.line.setData(self.time, self.response)
            self.timeBuffer = []
            self.responseBuffer = []

    def setupTimer(self):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.sampleTime)
        self.timer.timeout.connect(self.updatePlot)
        self.timer.start()

    def changeTimerInterval(self):
        '''
        Toggle the timer and reset the interval
        '''
        self.timer.stop()
        self.timer.setInterval(self.sampleTime)
        self.timer.start()
