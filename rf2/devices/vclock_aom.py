from rf2.devices.n5100 import N5100, N5100Proxy


class Device(N5100):
    _amplitude_range = (-20, 20)
    _amplitude_units = 'dBm'
    _frequency_range = (40e6, 70e6)
    _vxi11_address = '192.168.1.10'

class DeviceProxy(Device, N5100Proxy):
    _vxi11_servername = 'yesr10_vxi11'
    
    def __init__(self, cxn=None, **kwargs):
        N5100Proxy.__init__(self, cxn=cxn, **kwargs)
