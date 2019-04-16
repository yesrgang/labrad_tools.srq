from camera.clients.default import CameraClient

class MicroscopeClient(CameraClient):
    name = 'microscope'


if __name__ == '__main__':
    from PyQt4 import QtGui
    app = QtGui.QApplication([])
    import client_tools.qt4reactor as qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor
    widget = MicroscopeClient(reactor)
    widget.show()
    reactor.run()
