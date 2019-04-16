from rf2.devices.keysight336xx import Keysight336xx, Keysight336xxProxy

class Device(Keysight336xx):
    
    _amplitude_range = (-20, 20)
    _amplitude_units = 'dBm'
    _frequency_range = (250e3, 120e6)
    _source = 1
    _vxi11_address = "192.168.1.3"

class DeviceProxy(Device, Keysight336xxProxy):
    _vxi11_servername = 'yesr10_vxi11'
    
    def __init__(self, cxn=None, **kwargs):
        Keysight336xxProxy.__init__(self, cxn=cxn, **kwargs)
