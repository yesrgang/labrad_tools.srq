from rf2.devices.dg4000 import DG4000, DG4000Proxy

class Device(DG4000):
    _amplitude_range = (0.0, 5.0)
    _amplitude_units = 'V'
    _frequency_range = (0, 160e6)
    _source = 2
    _vxi11_address = '192.168.1.40'

class DeviceProxy(Device, DG4000Proxy):
    _vxi11_servername = 'yesr10_vxi11'
    
    def __init__(self, cxn=None, **kwargs):
        DG4000Proxy.__init__(self, cxn=cxn, **kwargs)
