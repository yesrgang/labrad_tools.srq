from picomotor.clients.picomotor_client import MultipleWidgetsContainer
from picomotor.clients.picomotor_client import PicomotorClient


class HODTXClient(PicomotorClient):
    name = 'hodt_x'
    servername = 'picomotor'
    position_range = [-1e5, 1e5]
    update_time = 100
    spinbox_width = 70

class HODTYClient(PicomotorClient):
    name = 'hodt_y'
    servername = 'picomotor'
    position_range = [-1e5, 1e5]
    update_time = 100
    spinbox_width = 70

class VODTXClient(PicomotorClient):
    name = 'vodt_x'
    servername = 'picomotor'
    position_range = [-1e5, 1e5]
    update_time = 100
    spinbox_width = 70

class VODTYClient(PicomotorClient):
    name = 'vodt_y'
    servername = 'picomotor'
    position_range = [-1e5, 1e5]
    update_time = 100
    spinbox_width = 70

class TransXClient(PicomotorClient):
    name = 'trans_x'
    servername = 'picomotor'
    position_range = [-1e5, 1e5]
    update_time = 100
    spinbox_width = 70

class TransYClient(PicomotorClient):
    name = 'trans_y'
    servername = 'picomotor'
    position_range = [-1e5, 1e5]
    update_time = 100
    spinbox_width = 70

class ImageXClient(PicomotorClient):
    name = 'image_x'
    servername = 'picomotor'
    position_range = [-1e5, 1e5]
    update_time = 100
    spinbox_width = 70

class ImageYClient(PicomotorClient):
    name = 'image_y'
    servername = 'picomotor'
    position_range = [-1e5, 1e5]
    update_time = 100
    spinbox_width = 70

class OSGXClient(PicomotorClient):
    name = 'osg_x'
    servername = 'picomotor'
    position_range = [-1e5, 1e5]
    update_time = 100
    spinbox_width = 70

class OSGYClient(PicomotorClient):
    name = 'osg_y'
    servername = 'picomotor'
    position_range = [-1e5, 1e5]
    update_time = 100
    spinbox_width = 70

class SideImageXClient(PicomotorClient):
    name = 'side_image_x'
    servername = 'picomotor'
    position_range = [-1e5, 1e5]
    update_time = 100
    spinbox_width = 70

class SideImageYClient(PicomotorClient):
    name = 'side_image_y'
    servername = 'picomotor'
    position_range = [-1e5, 1e5]
    update_time = 100
    spinbox_width = 70

class SideProbeXClient(PicomotorClient):
    name = 'side_probe_x'
    servername = 'picomotor'
    position_range = [-1e5, 1e5]
    update_time = 100
    spinbox_width = 70

class SideProbeYClient(PicomotorClient):
    name = 'side_probe_y'
    servername = 'picomotor'
    position_range = [-1e5, 1e5]
    update_time = 100
    spinbox_width = 70

class MyWidgetContainer(MultipleWidgetsContainer):
    name = 'xodt positions'
    widgets = [
        (HODTXClient, HODTYClient),
        (VODTXClient, VODTYClient),
        (TransXClient, TransYClient),
        (ImageXClient, ImageYClient),
        (OSGXClient, OSGYClient),
        (SideImageXClient, SideImageYClient),
        (SideProbeXClient, SideProbeYClient),
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
