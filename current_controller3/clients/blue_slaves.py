from current_controller3.devices._3d import DeviceProxy as _3DProxy
from current_controller3.devices._2d import DeviceProxy as _2DProxy
from current_controller3.devices.zs import DeviceProxy as ZSProxy
from current_controller3.devices._3d2 import DeviceProxy as _3D2Proxy
from current_controller3.devices._3d3 import DeviceProxy as _3D3Proxy
from current_controller3.clients.default import CurrentControllerClient
from current_controller3.clients.default import MultipleClientContainer


class _3DClient(CurrentControllerClient):
    DeviceProxy = _3DProxy
    name = '3d'

class _2DClient(CurrentControllerClient):
    DeviceProxy = _2DProxy
    name = '2d'

class ZSClient(CurrentControllerClient):
    DeviceProxy = ZSProxy
    name = 'zs'

class _3D2Client(CurrentControllerClient):
    DeviceProxy = _3D2Proxy
    name = '3d2'

class _3D3Client(CurrentControllerClient):
    DeviceProxy = _3D3Proxy
    name = '3d3'

class MyClientContainer(MultipleClientContainer):
    name = 'blue slaves'

if __name__ == '__main__':
    from PyQt4 import QtGui
    app = QtGui.QApplication([])
    from client_tools import qt4reactor 
    qt4reactor.install()
    from twisted.internet import reactor

    widgets = [_3DClient(reactor), _2DClient(reactor), ZSClient(reactor), _3D2Client(reactor), _3D3Client(reactor)]
    widget = MyClientContainer(widgets, reactor)
    widget.show()
    reactor.run()
