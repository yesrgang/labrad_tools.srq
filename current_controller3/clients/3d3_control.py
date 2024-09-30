from current_controller3.clients.default import MultipleClientContainer
from current_controller3.clients.default import CurrentControllerClient
from current_controller3.devices._3d3 import DeviceProxy as _3D3Proxy


class _3D3Client(CurrentControllerClient):
    DeviceProxy = _3D3Proxy
    name = '3d3'

class MyClientContainer(MultipleClientContainer):
    name = '3D3 controller'

if __name__ == '__main__':
    from PyQt4 import QtGui
    app = QtGui.QApplication([])
    from client_tools import qt4reactor 
    qt4reactor.install()
    from twisted.internet import reactor

    widgets = [_3D3Client(reactor)]
    widget = MyClientContainer(widgets, reactor)
    widget.show()
    reactor.run()
