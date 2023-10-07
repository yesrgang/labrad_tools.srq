import contextlib
import glob
import h5py
from io import StringIO
import numpy as np
import os
from PyQt4 import QtGui
import sys
from twisted.internet.defer import inlineCallbacks
import json
from client_tools.connection import connection
        
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import scipy as sp
from scipy import optimize


PIXEL_SIZE = 1.1e-6
CROSS_SECTION = 0.1014e-12 * 0.46
LINEWIDTH = 32e6 * 0.89
PULSE_LENGTH = 5e-6
GAIN = 5.2
DATADIR = "Q:\\data\\"
SCRIPTDIR = "Q:\\scripts\\"

@contextlib.contextmanager
def stdoutIO():
    old = sys.stdout
    stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old
        
class Client(QtGui.QWidget):

    def __init__(self, reactor):
        super(Client, self).__init__()
        self.reactor = reactor
        self.update_id = np.random.randint(0, 2**31 - 1)

        self.populate()
        self.connect()

    def populate(self):
        self.imagePathBox = QtGui.QLineEdit()
        self.imagePathBox.setFixedWidth(300)

        self.processPathBox = QtGui.QLineEdit()
        self.processPathBox.setFixedWidth(300)

        self.scriptBox = QtGui.QTextEdit()
        self.scriptBox.setReadOnly(True)
        self.scriptBox.setFixedHeight(100)
        self.scriptBox.setFixedWidth(300)
        
        self.outputBox = QtGui.QTextEdit()
        self.outputBox.setReadOnly(True)
        self.outputBox.setFixedHeight(100)
        self.outputBox.setFixedWidth(300)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.figure.add_subplot(111)
        self.figure.get_axes()[0].set_xlim(0, 1024)
        self.figure.get_axes()[0].set_ylim(0, 1024)

        self.layout = QtGui.QGridLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.imagePathBox, 0, 0, 1, 1)
        self.layout.addWidget(self.processPathBox, 1, 0)
        self.layout.addWidget(self.scriptBox, 2, 0)
        self.layout.addWidget(self.outputBox, 3, 0)
        self.layout.addWidget(self.toolbar, 0, 1)
        self.layout.addWidget(self.canvas, 1, 1, 4, 1)
        self.setLayout(self.layout)
        self.setWindowTitle("Ikon Viewer")

        self.imagePathBox.returnPressed.connect(self.displayImage)
#        self.processPathBox.returnPressed.connect(self.updateProcess)
#        self.updateProcess()
        
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
                self.imagePathBox.setText(value)
                self.displayImage()

    def getImagePath(self):
        text = str(self.imagePathBox.text())
        if text:
            return sorted(glob.glob(os.path.join(DATADIR, text)))[-1]
    
    def displayImage(self):
        image_path = sorted(glob.glob(os.path.join(DATADIR, str(self.imagePathBox.text()))))[-1]
        process_path = os.path.join(SCRIPTDIR, str(self.processPathBox.text()))
#        old_stdout = sys.stdout
#        old_errout = sys.errout
#        stdout = sys.stdout = StringIO()
        if os.path.isfile(process_path):
            f = open(process_path, 'r')
            try:
                exec(f.read())
            except:
                raise
            finally:
                f.close()
        else:
            print(':(')
#        self.outputBox.setText(s.getvalue())

#    def updateProcess(self):
#        process_path = os.path.join(SCRIPTDIR, str(self.processPathBox.text()))
#        if os.path.isfile(process_path):
#            with open(process_path, 'r') as f:
#                self.scriptBox.setText(f.read())
#        else:
#            print(process_path)
#        
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
