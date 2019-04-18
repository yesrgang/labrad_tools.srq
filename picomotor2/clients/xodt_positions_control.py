from picomotor2.devices import hodt_x
from picomotor2.devices import hodt_y
from picomotor2.devices import vodt_x
from picomotor2.devices import vodt_y
from picomotor2.devices import trans_x
from picomotor2.devices import trans_y
from picomotor2.devices import image_x
from picomotor2.devices import image_y
from picomotor2.devices import osg_x
from picomotor2.devices import osg_y
from picomotor2.clients.default import MultipleClientContainer, PicomotorClient


class HODTXClient(PicomotorClient):
    DeviceProxy = hodt_x.DeviceProxy
    name = 'hodt_x'

class HODTYClient(PicomotorClient):
    DeviceProxy = hodt_y.DeviceProxy
    name = 'hodt_y'

class VODTXClient(PicomotorClient):
    DeviceProxy = vodt_x.DeviceProxy
    name = 'vodt_x'

class VODTYClient(PicomotorClient):
    DeviceProxy = vodt_y.DeviceProxy
    name = 'vodt_y'

class TransXClient(PicomotorClient):
    DeviceProxy = trans_x.DeviceProxy
    name = 'trans_x'

class TransYClient(PicomotorClient):
    DeviceProxy = trans_y.DeviceProxy
    name = 'trans_y'

class ImageXClient(PicomotorClient):
    DeviceProxy = image_x.DeviceProxy
    name = 'image_x'

class ImageYClient(PicomotorClient):
    DeviceProxy = image_y.DeviceProxy
    name = 'image_y'

class OSGXClient(PicomotorClient):
    DeviceProxy = osg_x.DeviceProxy
    name = 'osg_x'

class OSGYClient(PicomotorClient):
    DeviceProxy = osg_y.DeviceProxy
    name = 'osg_y'

class Client(MultipleClientContainer):
    name = 'xodt positions'
    children = [
        (HODTXClient, HODTYClient),
        (VODTXClient, VODTYClient),
        (TransXClient, TransYClient),
        (ImageXClient, ImageYClient),
        (OSGXClient, OSGYClient),
        ]

if __name__ == '__main__':
    from PyQt4 import QtGui
    app = QtGui.QApplication([])
    from client_tools import qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor
    
    widget = Client(reactor)
    widget.show()
    reactor.run()
