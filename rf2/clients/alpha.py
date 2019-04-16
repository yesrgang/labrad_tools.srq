from rf2.clients.default import RFClient
from rf2.devices import alpha

class Client(RFClient):
    DeviceProxy = alpha.DeviceProxy
    amplitudeDigits = 2
    frequencyDigits = 6
    frequencyDisplayUnits = [(9, 'GHz')]
    name = 'alpha'

if __name__ == '__main__':
    from PyQt4 import QtGui
    app = QtGui.QApplication([])
    from client_tools import qt4reactor 
    qt4reactor.install()
    from twisted.internet import reactor

    widget = Client(reactor)
    widget.show()
    reactor.run()
