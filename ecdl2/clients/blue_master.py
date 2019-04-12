from ecdl2.devices.blue_master import DeviceProxy as BlueMasterProxy
from ecdl2.clients.default import ECDLClient


class BlueMasterClient(ECDLClient):
    name = 'blue_master'
    DeviceProxy = BlueMasterProxy
    
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

    widget = BlueMasterClient(reactor)
    widget.show()
    reactor.run()

