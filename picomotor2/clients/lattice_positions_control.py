from picomotor2.devices import h1_x
from picomotor2.devices import h1_y
from picomotor2.devices import h2_x
from picomotor2.devices import h2_y
from picomotor2.devices import h1_xr
from picomotor2.devices import h1_yr
from picomotor2.devices import h2_xr
from picomotor2.devices import h2_yr
from picomotor2.devices import v_x
from picomotor2.devices import v_y
from picomotor2.clients.default import MultipleClientContainer, PicomotorClient


class H1XClient(PicomotorClient):
    DeviceProxy = h1_x.DeviceProxy
    name = 'h1_x'

class H1YClient(PicomotorClient):
    DeviceProxy = h1_y.DeviceProxy
    name = 'h1_y'

class H2XClient(PicomotorClient):
    DeviceProxy = h2_x.DeviceProxy
    name = 'h2_x'

class H2YClient(PicomotorClient):
    DeviceProxy = h2_y.DeviceProxy
    name = 'h2_y'

class H1XRClient(PicomotorClient):
    DeviceProxy = h1_xr.DeviceProxy
    name = 'h1_xr'

class H1YRClient(PicomotorClient):
    DeviceProxy = h1_yr.DeviceProxy
    name = 'h1_yr'

class H2XRClient(PicomotorClient):
    DeviceProxy = h2_xr.DeviceProxy
    name = 'h2_xr'

class H2YRClient(PicomotorClient):
    DeviceProxy = h2_yr.DeviceProxy
    name = 'h2_yr'

class VXClient(PicomotorClient):
    DeviceProxy = v_x.DeviceProxy
    name = 'v_x'

class VYClient(PicomotorClient):
    DeviceProxy = v_y.DeviceProxy
    name = 'v_y'

class Client(MultipleClientContainer):
    name = 'lattice positions'
    children = [
        (H1XClient, H1YClient),
        (H2XClient, H2YClient),
        (H1XRClient, H1YRClient),
        (H2XRClient, H2YRClient),
        (VXClient, VYClient),
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
