from rf2.clients.default import RFClient
from rf2.devices import beta

class Client(RFClient):
    DeviceProxy = beta.DeviceProxy
    amplitudeDigits = 2
    frequencyDigits = 3
    frequencyDisplayUnits = [(6, 'MHz')]
    name = 'beta'

if __name__ == '__main__':
    from PyQt4 import QtGui
    app = QtGui.QApplication([])
    from client_tools import qt4reactor 
    qt4reactor.install()
    from twisted.internet import reactor

    widget = Client(reactor)
    widget.show()
    reactor.run()
