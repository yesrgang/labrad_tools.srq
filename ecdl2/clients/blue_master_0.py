from ecdl2.devices.blue_master_0 import DeviceProxy as BlueMaster0Proxy
from ecdl2.clients.default import ECDLClient


class BlueMasterClient(ECDLClient):
    name = 'blue_master_0'
    DeviceProxy = BlueMaster0Proxy
    
    spinboxWidth = 80
    piezoVoltageDisplayUnits = [(0, 'V')]
    piezoVoltageDigits = 2
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

