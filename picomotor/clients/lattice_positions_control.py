from picomotor.clients.picomotor_client import MultipleWidgetsContainer
from picomotor.clients.picomotor_client import PicomotorClient


class H1XClient(PicomotorClient):
    name = 'h1_x'
    servername = 'picomotor'
    position_range = [-1e5, 1e5]
    update_time = 100
    spinbox_width = 70

class H1YClient(PicomotorClient):
    name = 'h1_y'
    servername = 'picomotor'
    position_range = [-1e5, 1e5]
    update_time = 100
    spinbox_width = 70

class H2XClient(PicomotorClient):
    name = 'h2_x'
    servername = 'picomotor'
    position_range = [-1e5, 1e5]
    update_time = 100
    spinbox_width = 70

class H2YClient(PicomotorClient):
    name = 'h2_y'
    servername = 'picomotor'
    position_range = [-1e5, 1e5]
    update_time = 100
    spinbox_width = 70

class H1XRClient(PicomotorClient):
    name = 'h1_xr'
    servername = 'picomotor'
    position_range = [-1e5, 1e5]
    update_time = 100
    spinbox_width = 70

class H1YRClient(PicomotorClient):
    name = 'h1_yr'
    servername = 'picomotor'
    position_range = [-1e5, 1e5]
    update_time = 100
    spinbox_width = 70

class H2XRClient(PicomotorClient):
    name = 'h2_xr'
    servername = 'picomotor'
    position_range = [-1e5, 1e5]
    update_time = 100
    spinbox_width = 70

class H2YRClient(PicomotorClient):
    name = 'h2_yr'
    servername = 'picomotor'
    position_range = [-1e5, 1e5]
    update_time = 100
    spinbox_width = 70

class VXClient(PicomotorClient):
    name = 'v_x'
    servername = 'picomotor'
    position_range = [-1e5, 1e5]
    update_time = 100
    spinbox_width = 70

class VYClient(PicomotorClient):
    name = 'v_y'
    servername = 'picomotor'
    position_range = [-1e5, 1e5]
    update_time = 100
    spinbox_width = 70

class MyWidgetContainer(MultipleWidgetsContainer):
    name = lattice_positions
    widgets = [
        (H1XClient, H1YClient),
        (H2XClient, H2YClient),
        (H1XRClient, H1YRClient),
        (H2XRClient, H2YRClient),
        (VXClient, VYClient),
        ]

Client = MyWidgetContainer

if __name__ == '__main__':
    from PyQt4 import QtGui
    app = QtGui.QApplication([])
    from client_tools import qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor
    widget = Client(reactor)
    widget.show()
    reactor.run()
