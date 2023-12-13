import pyqtgraph as pg
from PyQt5 import QtCore
import Geophone

class Seismograph(pg.PlotWidget):

    def __init__(self, parent=None):
        super(Seismograph, self).__init__(parent)
        #TODO: set up geophone here I would think
        #      need to think about this
        self._updateTime = 1.0

    @property(int)
    def updateTime(self) -> int:
        return self._updateTime

    @updateTime.setter(int)
    def updateTime(self, value:int):
        self._updateTime = value

    @property(int)
    def updateLength(self):
        return int(self.updateTime / self.geo.sampleTime)

    def updatePlot(self):
        # My thoughts here are:
        # We should update the plots at a regular frequency, but maybe not at the
        # read frequency of the sample time. so something like (updateTime/sampleTime)
        # points of data

        # Move buffer up by sampled data points
        # What does a full day of samples look like. should we start scrolling??
        if len(timePlot) < fullDay:
            self.timePlot.append(self.timeBuffer)
            self.seisPlot.append(self.seisBuffer)
        else:
            self.timePlot = self.timePlot[self.updateLength:] 
            self.timePlot.append(self.timeBuffer)
            self.seisPlot = self.seisPlot[self.updateLength:]
            self.seisPlot.append(self.seisBuffer)

    def setupTimer(self):

        self.timer = QtCore.QTimer()
        self.time.setInterval(self.updateTime)
        self.timer.timeout.connect(self.updatePlot)
        self.time.start()
