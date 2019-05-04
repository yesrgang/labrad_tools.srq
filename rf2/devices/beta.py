from rf2.devices.keysight33600 import Keysight33600, Keysight33600Proxy

class Device(Keysight33600):
    
    _amplitude_range = (-20, 20)
    _amplitude_units = 'dBm'
    _frequency_range = (250e3, 120e6)
    _source = 1
    _vxi11_address = "192.168.1.3"

class DeviceProxy(Device, Keysight33600Proxy):
    _vxi11_servername = 'yesr10_vxi11'
    
    def __init__(self, cxn=None, **kwargs):
        Keysight33600Proxy.__init__(self, cxn=cxn, **kwargs)
