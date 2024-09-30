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
        
def gauss2(xy, a, b, x0, y0, sx, sy):
    (x, y) = xy
    theta = 0
    A = (np.cos(theta)**2 / (2 * sx**2) + np.sin(theta)**2 / (2 * sy**2)) * 4
    B = (-np.sin(2 * theta) / (4 * sx**2) + np.sin(2 * theta) / (4 * sy**2)) * 4
    C = (np.sin(theta)**2 / (2 * sx**2) + np.cos(theta)**2 / (2 * sy**2)) * 4
    return a * np.exp(-A * (x - x0)**2 - 2 * B * (x - x0) * (y - y0) - C * (y - y0)**2) + b

def f0(x):
    return np.exp(-x) / (1 + np.exp(-x))

def f1(x):
    return np.log(1 + np.exp(-x))

def f2(x):
    return -1 * sp.special.spence(1 + np.exp(-x))

def f3(x):
    return float(-1 * mpmath.polylog(3, -np.exp(-x)))

def f4(x):
    return float(-1 * mpmath.polylog(4, -np.exp(-x)))

def fermi2(xy, a, b, x0, y0, rx, ry, q):
    (x, y) = xy
    return 4 * a * f2(((x - x0)**2 / rx**2 + (y - y0)**2 / ry**2) * f1(-q) / f0(-q) - q) / f3(-q) + b



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
        self.processBox.addItem('Fluorescence Image')
        self.processBox.addItem('Absorption Counts')
        self.processBox.addItem('Absorption Image')
        self.processBox.addItem('Absorption Bright')

        self.parameterBox = QtGui.QTextEdit()
        self.parameterBox.setText(
            "x0, y0 = 512, 512\n"
            "x, y = np.meshgrid(range(1024), range(1024))\n"
            "r2 = (x - x0)**2 + (y - y0)**2\n"
            "cloud = (r2 < 512**2)\n"
            "norm = (r2 > 512**2) & (r2 < np.inf**2)\n"
            "fit=False\n"
            "FD=False\n"
            )
        self.parameterBox.setFixedHeight(100)
        self.parameterBox.setFixedWidth(300)
        
        self.outputBox = QtGui.QTextEdit()
        self.outputBox.setReadOnly(True)
        self.outputBox.setFixedHeight(100)
        self.outputBox.setFixedWidth(300)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        ax = self.figure.add_subplot(111)
        ax.set_xlim(0, 1023)
        ax.set_ylim(0, 1023)

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
        self.setWindowTitle("Ikon Viewer")

        self.pathBox.returnPressed.connect(self.displayImage)
        self.processBox.currentIndexChanged.connect(self.updateProcess)

        self.updateProcess()
        
    @inlineCallbacks
    def connect(self):
        self.cxn = connection()
        yield self.cxn.connect(name='ikon viewer')
        server = yield self.cxn.get_server('conductor')
        yield server.signal__update(self.update_id)
        yield server.addListener(listener=self.receive_update, source=None, ID=self.update_id)

    def receive_update(self, c, update_json):
        update = json.loads(update_json)
        for key, value in update.items():
            if key == 'andor.record_path':
                self.pathBox.setText(value)
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
        fit = False
        FD = False
        exec(self.getParameters())
        h5f = h5py.File(os.path.join(DATADIR, "20210124/abs-ref#1/avg.ikon.hdf5"), "r")
        ref_image = np.array(h5f['image'], dtype='float')
        ref_bright = np.array(h5f['bright'], dtype='float')
        h5f.close()
        

        h5f = h5py.File(image_path, "r")
        image = np.array(h5f['image'], dtype='float') - ref_image
        bright = np.array(h5f['bright'], dtype='float') - ref_bright
        h5f.close()

        bright *= image[norm].mean() / bright[norm].mean()

        od = np.zeros_like(image)
        diff = np.zeros_like(image)
        i = (image > 0) & (bright > 0)
        od[i] = np.log(bright[i] / image[i])
        diff[i] = bright[i] - image[i]
        counts = od * PIXEL_SIZE**2 / CROSS_SECTION + diff * GAIN / (np.pi * LINEWIDTH * PULSE_LENGTH)

        tot = counts[cloud].sum()
        zoom = ((x - x0)**2 <= 50**2) & ((y - y0)**2  <= 50**2)
        xfit, yfit = 0, 0
        if fit:
            p0 = (300, 0, x0, y0, 30, 30)
            bounds = (
                [0, -np.inf, 0, 0, 0, 0],
                [np.inf, np.inf, 1024, 1024, np.inf, np.inf]
                )
            popt, pcov = sp.optimize.curve_fit(
                    gauss2, (x[cloud], y[cloud]), counts[cloud], p0=p0, 
                    bounds=bounds, maxfev=1000)
            
            xfit, yfit = popt[2], popt[3]
            xsize,ysize = popt[4], popt[5]
            rms_size = np.sqrt(xsize**2+ysize**2)
            fitted_cloud = gauss2((x[zoom], y[zoom]), popt[0], popt[1], popt[2], popt[3], popt[4], popt[5])
            fitted_cloud_imshow = fitted_cloud.reshape((101, 101))
#            p0 = (popt[0], popt[1], popt[2], popt[3], popt[4], popt[5], 10)
#            bounds = ([0, -np.inf, 0, 0, 0, 0, -np.inf],[p0[0] * 20, np.inf, 1024, 1024, np.inf, np.inf, np.inf])
#            popt_fermi, pcov_fermi = sp.optimize.curve_fit(fermi2, (x[cloud], y[cloud]),
#                                           counts[cloud],
#                                           p0=p0,
#                                            bounds=bounds,
#                                           maxfev=10000)
#            fermi_fit = fermi2((x, y), popt_fermi[0], popt_fermi[1], popt_fermi[2], popt_fermi[3], popt_fermi[4], popt_fermi[5], popt_fermi[6])
           
#            ttf = (6 * f3(-popt_fermi[-1]))**(-1 / 3)
            if FD:
                p0 = (popt[0], popt[1], popt[2], popt[3], popt[4], popt[5], 10)
                bounds = ([0, -np.inf, 0, 0, 0, 0, -np.inf],[p0[0] * 20, np.inf, 1024, 1024, np.inf, np.inf, np.inf])
                popt_fermi, pcov_fermi = sp.optimize.curve_fit(fermi2, (x[cloud], y[cloud]),
                                            counts[cloud],
                                            p0=p0,
                                            bounds=bounds,
                                            maxfev=10000)
                fermi_fit = fermi2((x, y), popt_fermi[0], popt_fermi[1], popt_fermi[2], popt_fermi[3], popt_fermi[4], popt_fermi[5], popt_fermi[6])
           
                ttf = (6 * f3(-popt_fermi[-1]))**(-1 / 3)

                fitted_cloud = fermi2((x[zoom], y[zoom]),  popt_fermi[0], popt_fermi[1], popt_fermi[2], popt_fermi[3], popt_fermi[4], popt_fermi[5], popt_fermi[6])
                fitted_cloud_imshow = fitted_cloud.reshape((101, 101))
                self.outputBox.setText("Total Counts: {:.2e}\n".format(tot)+ "Fit Center: {:.1f}, {:.1f}\n".format(xfit, yfit))
                                        )





        self.outputBox.setText("Total Counts: {:.2e}\n".format(tot)+ "Fit Center: {:.1f}, {:.1f}\n".format(xfit, yfit))


        
        xmin, xmax = self.figure.get_axes()[0].get_xlim()
        ymin, ymax = self.figure.get_axes()[0].get_ylim() 
        self.figure.clear()


        if fit:
            ax = self.figure.add_subplot(121)
            ax.imshow(image, cmap='inferno', origin='lower')
            ax.set_xlim(xmin, xmax)
            ax.set_ylim(ymin, ymax)
            ax.contour(norm, colors='r')
            ax.contour(cloud, colors='w')
            ax2 = self.figure.add_subplot(222)
            ax2.plot(np.sum(counts[zoom].reshape((101, 101)), axis = 0), color = 'black')
            ax2.plot(np.sum(fitted_cloud_imshow, axis = 0), '--', color = 'red', alpha = .5)
           # ax2.set_xlim(xmin, xmax)
            ax3 = self.figure.add_subplot(224)
            ax3.plot(np.sum(coounts[zoom].reshape((101, 101)), axis = 1), color = 'black')
            ax3.plot(np.sum(fitted_cloud_imshow, axis = 1), '--', color = 'red', alpha = .5)
            #ax3.set_xlim(ymin, ymax)

            self.canvas.draw()
        else:
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
        h5f = h5py.File(os.path.join(DATADIR, "20210121/abs-ref#0/ref.ikon.hdf5"), "r")
        ref_image = np.array(h5f['image'], dtype='float')
        ref_bright = np.array(h5f['bright'], dtype='float')
        h5f.close()

        h5f = h5py.File(image_path, "r")
        image = np.array(h5f['image'], dtype='float') - ref_image
        bright = np.array(h5f['bright'], dtype='float') - ref_bright
        h5f.close()
        xmin, xmax = self.figure.get_axes()[0].get_xlim()
        ymin, ymax = self.figure.get_axes()[0].get_ylim() 
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.imshow(image, cmap='inferno', origin='lower')
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
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
        h5f = h5py.File(os.path.join(DATADIR, "20210121/abs-ref#0/ref.ikon.hdf5"), "r")
        ref_image = np.array(h5f['image'], dtype='float')
        ref_bright = np.array(h5f['bright'], dtype='float')
        h5f.close()

        h5f = h5py.File(image_path, "r")
        image = np.array(h5f['image'], dtype='float') - ref_image
        bright = np.array(h5f['bright'], dtype='float') - ref_bright
        h5f.close()
        
        xmin, xmax = self.figure.get_axes()[0].get_xlim()
        ymin, ymax = self.figure.get_axes()[0].get_ylim()
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.imshow(bright, cmap='inferno', origin='lower')
        ax.contour(norm, colors='r')
        ax.contour(cloud, colors='w')
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        self.canvas.draw()

    def processFluorescenceImage(self, image_path):
        exec(self.getParameters())
#        h5f = h5py.File(os.path.join(DATADIR, "20210121/abs-ref#0/ref.ikon.hdf5"), "r")
#        ref_image = np.array(h5f['image'], dtype='float')
#        ref_bright = np.array(h5f['bright'], dtype='float')
#        h5f.close()

        h5f = h5py.File(image_path, "r")
        image = np.array(h5f['image'], dtype='float') #- ref_image
#        bright = np.array(h5f['bright'], dtype='float') #- ref_bright
        h5f.close()
        
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.imshow(image, cmap='inferno', origin='lower')
#        ax.contour(norm, colors='r')
        ax.contour(cloud, colors='w')
        self.canvas.draw()

    def setupFluorescenceImage(self):
        exec(self.getParameters())
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_xlim(0, 1023)
        ax.set_ylim(0, 1023)
#        ax.contour(norm, colors='r')
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
        elif self.processBox.currentText() == "Fluorescence Image":
            self.processFluorescenceImage(image_path)
    
    def updateProcess(self):
        if self.processBox.currentText() == "Absorption Counts":
            self.setupAbsorptionCounts()
        if self.processBox.currentText() == "Absorption Image":
            self.setupAbsorptionImage()
        if self.processBox.currentText() == "Absorption Bright":
            self.setupAbsorptionBright()
        if self.processBox.currentText() == "Fluorescence Image":
            self.setupFluorescenceImage()

    def ckiseEvent(self, x):
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
