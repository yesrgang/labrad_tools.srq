from current_controller3.devices._3d import DeviceProxy as _3DProxy
from current_controller3.devices._2d import DeviceProxy as _2DProxy
from current_controller3.devices.zs import DeviceProxy as ZSProxy
from current_controller3.clients.default import CurrentControllerClient
from current_controller3.clients.default import MultipleClientContainer


class _3DClient(CurrentControllerClient):
    name = '3d'
    update_time = 200
    DeviceProxy = _3DProxy

class _2DClient(CurrentControllerClient):
    name = '2d'
    update_time = 200
    DeviceProxy = _2DProxy

class ZSClient(CurrentControllerClient):
    name = 'zs'
    update_time = 200
    DeviceProxy = ZSProxy

class MyClientContainer(MultipleClientContainer):
    name = 'blue slaves'

if __name__ == '__main__':
    from PyQt4 import QtGui
    app = QtGui.QApplication([])
    from client_tools import qt4reactor 
    qt4reactor.install()
    from twisted.internet import reactor

    channels = ['3d', '2d', 'zs']
    widgets = [_3DClient(reactor), _2DClient(reactor), ZSClient(reactor)]
    widget = MyClientContainer(widgets, reactor)
    widget.show()
    reactor.run()
