from current_controller.clients.default import MultipleClientContainer
from current_controller.clients.default import CurrentControllerClient

class Client3D(CurrentControllerClient):
    name = '3d'
    servername = 'current_controller'
    update_time = 100

class Client2D(CurrentControllerClient):
    name = '2d'
    servername = 'current_controller'
    update_time = 100

class ClientZS(CurrentControllerClient):
    name = 'zs'
    servername = 'current_controller'
    update_time = 100

class MyClientContainer(MultipleClientContainer):
    name = 'blue slaves'

if __name__ == '__main__':
    from PyQt4 import QtGui
    app = QtGui.QApplication([])
    from client_tools import qt4reactor 
    qt4reactor.install()
    from twisted.internet import reactor

    channels = ['3d', '2d', 'zs']
    widgets = [Client3D(reactor), Client2D(reactor), ClientZS(reactor)]
    widget = MyClientContainer(widgets, reactor)
#    app.setStyle(QtGui.QStyleFactory.create(widget.qt_style))
    widget.show()
    reactor.run()
