from picomotor2.devices.nf8742 import NF8742, NF8742Proxy

class Device(NF8742):
    _socket_address = ('192.168.1.20', 23)
    _controller_axis = 1

class DeviceProxy(Device, NF8742Proxy):
    _socket_servername = 'yesr10_socket'

    def __init__(self, cxn=None, **kwargs):
        NF8742Proxy.__init__(self, cxn, **kwargs)
