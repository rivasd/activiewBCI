from ActiView import ActiveTwo
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

app = QtGui.QApplication([])
win = pg.GraphicsWindow()
win.setWindowTitle("Mimicking ActiView's EEG monitoring screen")


monitor = win.addPlot()

#we have so many curves that we will store them in an array
curves = [monitor.plot() for x in range(64)]

#this is the data that will be continuously updated and plotted
rawdata = np.empty((64,0))


#initialize connection with ActiView
actiview = ActiveTwo()

def update():
    global rawdata
    data = actiview.read()
    rawdata = np.concatenate((rawdata, data), axis=1)
    for i in range(64):
        curves[i].setData(rawdata[i])
    


timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)

if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1 or not hasattr(pg.QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()