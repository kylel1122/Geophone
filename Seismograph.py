import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets
from random import randint
#import Geophone


class Seismograph(pg.PlotWidget):
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')

    def __init__(self, update_time=1000, parent=None):
        super(Seismograph, self).__init__(parent)
        #TODO: set up geophone here I would think
        #      need to think about this
        self._updateTime = update_time
        self.setupPlot()
        self.setupTimer()


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

        self.time = list(range(10))
        self.response = [randint(0, 40) for _ in range(10)]

        self.line = self.seismo.plot(self.time,
                                     self.response,
                                     name='Response',
                                     pen=pen,
                                     symbol='+',
                                     symbolSize=15,
                                     symbolBrush='b',
                                     )



    @property
    def updateTime(self) -> float:
        return self._updateTime

    @updateTime.setter
    def updateTime(self, value:int):
        self._updateTime = value

    @property
    def updateLength(self):
        return int(self.updateTime / self.geo.sampleTime)

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
        self.time = self.time[1:]
        self.time.append(self.time[-1] +1)
        self.response = self.response[1:]
        self.response.append(randint(20,40))
        self.line.setData(self.time, self.response)

    def setupTimer(self):

        self.timer = QtCore.QTimer()
        self.timer.setInterval(int(self.updateTime))
        self.timer.timeout.connect(self.updatePlot)
        self.timer.start()

