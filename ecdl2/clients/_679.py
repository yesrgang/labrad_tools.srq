from ecdl2.devices import _679 
from ecdl2.clients.default import ECDLClient


class Client(ECDLClient):
    name = '679'
    DeviceProxy = _679.DeviceProxy
    
    spinboxWidth = 80
    piezoVoltageDisplayUnits = [(0, 'V')]
    piezoVoltageDigits = 1
    diodeCurrentDisplayUnits = [(0, 'mA')]
    diodeCurrentDigits = 1


if __name__ == '__main__':
    from PyQt4 import QtGui
    app = QtGui.QApplication([])
    from client_tools import qt4reactor 
    qt4reactor.install()
    from twisted.internet import reactor

    widget = Client(reactor)
    widget.show()
    reactor.run()

