import elliptec
reload(elliptec)
from elliptec import ELLO
from elliptec import ELLOProxy

class Device(ELLO):
    serial_port = '/dev/ttyUSB04036015'
    address = 0
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        ELLO.__init__(self)

class DeviceProxy(Device, ELLOProxy):
    serial_servername = 'yesr10_serial'

    def __init__(self, **kwargs):
        Device.__init__(self, **kwargs)
        ELLOProxy.__init__(self, self.serial_servername)
