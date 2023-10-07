import glob
import h5py
import numpy as np
import os
from PyQt4 import QtGui
from twisted.internet.defer import inlineCallbacks
import json
from client_tools.connection import connection
        
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import mpmath
import scipy as sp
from scipy import io
from scipy import optimize
#from scipy.special import spence
from scipy import special
from scipy import stats
import logging

PIXEL_SIZE = 1.1e-6
CROSS_SECTION = 0.1014e-12 * 0.46
LINEWIDTH = 32e6 * 0.89
PULSE_LENGTH = 5e-6
GAIN = 5.2
DATADIR = "Q:\\data\\"

class Client(QtGui.QWidget):

    def __init__(self, reactor):
        super(Client, self).__init__()
        self.reactor = reactor
        self.update_id = np.random.randint(0, 2**31 - 1)

        self.populate()
        self.connect()

    def populate(self):
        self.pathBox = QtGui.QLineEdit()

        self.processBox = QtGui.QComboBox()
        self.processBox.addItem('Absorption Counts')
        self.processBox.addItem('Absorption Image')
        self.processBox.addItem('Absorption Bright')
        self.processBox.addItem('Fluorescence Image')
        self.processBox.addItem('Dual Fluorescence Image')


        self.parameterBox = QtGui.QTextEdit()
        self.parameterBox.setText(
            "x0, y0 = 482, 646\n"
            "x, y = np.meshgrid(range(964), range(1292))\n"
            "r2 = (x - x0)**2 + (y - y0)**2\n"
            "cloud = (r2 < 646**2)\n"
            "norm = (r2 > 646**2) & (r2 < np.inf**2)\n"
            )
        self.parameterBox.setFixedHeight(100)
        self.parameterBox.setFixedWidth(300)
        
        self.outputBox = QtGui.QTextEdit()
#        self.outputBox.setFontPointSize(32)
        self.outputBox.setReadOnly(True)
        self.outputBox.setFixedHeight(500)
        self.outputBox.setFixedWidth(300)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        ax = self.figure.add_subplot(111)
        ax.set_xlim(0, 964)
        ax.set_ylim(0, 1292)


        self.layout = QtGui.QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.pathBox, 0, 0, 1, 2)
        self.layout.addWidget(self.processBox, 1, 0)
        self.layout.addWidget(self.parameterBox, 2, 0)
        self.layout.addWidget(self.outputBox, 3, 0)
        self.layout.addWidget(self.toolbar, 1, 1)
        self.layout.addWidget(self.canvas, 2, 1, 3, 1)
        self.setLayout(self.layout)
        self.setWindowTitle("Mako2 Viewer")

        self.pathBox.returnPressed.connect(self.displayImage)
        self.processBox.currentIndexChanged.connect(self.updateProcess)

        self.updateProcess()
        
    @inlineCallbacks
    def connect(self):
        self.cxn = connection()
        yield self.cxn.connect(name='mako2 viewer')
        server = yield self.cxn.get_server('yesr10_vimba')
        yield server.signal__update(self.update_id)
        yield server.addListener(listener=self.receive_update, source=None, ID=self.update_id)

    def receive_update(self, c, update):
        path = os.path.abspath(update).replace("C:\\home\\srgang\\srqdata\\", "Q:\\")
        self.pathBox.setText(path)
        self.displayImage()

    def getImagePath(self):
        text = str(self.pathBox.text())
        if text:
            return sorted(glob.glob(os.path.join(DATADIR, text)))[-1]

    def getParameters(self):
        return str(self.parameterBox.toPlainText())

    
    def setupAbsorptionCounts(self):
        xmin, xmax = self.figure.get_axes()[0].get_xlim()
        ymin, ymax = self.figure.get_axes()[0].get_ylim()
        exec(self.getParameters())
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        ax.contour(norm, colors='r')
        ax.contour(cloud, colors='w')
        self.canvas.draw()

    def processAbsorptionCounts(self, image_path):
        exec(self.getParameters())
#        h5f = h5py.File(os.path.join(DATADIR, "20210123", "ref.mako2.hdf5"), "r")
#        ref_image = np.array(h5f['image'], dtype='float')
#        ref_bright = np.array(h5f['bright'], dtype='float')
#        h5f.close()
        

        h5f = h5py.File(image_path, "r")
        image = np.array(h5f['image'], dtype='float') #- ref_image
        bright = np.array(h5f['bright'], dtype='float') #- ref_bright
        h5f.close()

        bright *= image[norm].mean() / bright[norm].mean()

        print(image.shape)

        od = np.zeros_like(image)
        diff = np.zeros_like(image)
        i = (image > 0) & (bright > 0)
        od[i] = np.log(bright[i] / image[i])
        diff[i] = bright[i] - image[i]
        counts = od * PIXEL_SIZE**2 / CROSS_SECTION + diff * GAIN / (np.pi * LINEWIDTH * PULSE_LENGTH)

        tot = counts[cloud].sum()

        self.outputBox.setText("Total Counts: {:.2e}\n".format(tot))

        xmin, xmax = self.figure.get_axes()[0].get_xlim()
        ymin, ymax = self.figure.get_axes()[0].get_ylim()
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.imshow(counts, cmap='inferno', origin='lower')
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        ax.contour(norm, colors='r')
        ax.contour(cloud, colors='w')
        self.canvas.draw()
    
    def setupAbsorptionImage(self):
        xmin, xmax = self.figure.get_axes()[0].get_xlim()
        ymin, ymax = self.figure.get_axes()[0].get_ylim()
        exec(self.getParameters())
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        ax.contour(norm, colors='r')
        ax.contour(cloud, colors='w')
        self.canvas.draw()
    
    def processAbsorptionImage(self, image_path):
        exec(self.getParameters())
#        h5f = h5py.File(os.path.join(DATADIR, "20210123/ref.mako2.hdf5"), "r")
#        ref_image = np.array(h5f['image'], dtype='float')
#        ref_bright = np.array(h5f['bright'], dtype='float')
#        h5f.close()

        h5f = h5py.File(image_path, "r")
        image = np.array(h5f['image'], dtype='float') #- ref_image
        bright = np.array(h5f['bright'], dtype='float') #- ref_bright
        h5f.close()
        
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.imshow(image, cmap='inferno', origin='lower')
        ax.contour(norm, colors='r')
        ax.contour(cloud, colors='w')
        self.canvas.draw()
    
    def setupAbsorptionBright(self):
        xmin, xmax = self.figure.get_axes()[0].get_xlim()
        ymin, ymax = self.figure.get_axes()[0].get_ylim()
        exec(self.getParameters())
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        ax.contour(norm, colors='r')
        ax.contour(cloud, colors='w')
        self.canvas.draw()
    
    def processAbsorptionBright(self, image_path):
        exec(self.getParameters())
#        h5f = h5py.File(os.path.join(DATADIR, "20210123/ref.mako2.hdf5"), "r")
#        ref_image = np.array(h5f['image'], dtype='float')
#        ref_bright = np.array(h5f['bright'], dtype='float')
#        h5f.close()

        h5f = h5py.File(image_path, "r")
        image = np.array(h5f['image'], dtype='float') #- ref_image
        bright = np.array(h5f['bright'], dtype='float') #- ref_bright
        h5f.close()
        
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.imshow(bright, cmap='inferno', origin='lower')
        ax.contour(norm, colors='r')
        ax.contour(cloud, colors='w')
        self.canvas.draw()
    
    def displayImage(self):
        image_path = self.getImagePath()
        if self.processBox.currentText() == "Absorption Counts":
            self.processAbsorptionCounts(image_path)
        elif self.processBox.currentText() == "Absorption Image":
            self.processAbsorptionImage(image_path)
        elif self.processBox.currentText() == "Absorption Bright":
            self.processAbsorptionBright(image_path)
    
    def updateProcess(self):
        if self.processBox.currentText() == "Absorption Counts":
            self.setupAbsorptionCounts()
        if self.processBox.currentText() == "Absorption Image":
            self.setupAbsorptionImage()
        if self.processBox.currentText() == "Absorption Bright":
            self.setupAbsorptionBright()

    def closeEvent(self, x):
        self.reactor.stop()

if __name__ == '__main__':
    from PyQt4 import QtGui
    app = QtGui.QApplication([])
    import client_tools.qt4reactor as qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor
    widget = Client(reactor)
    widget.show()
    reactor.run()
