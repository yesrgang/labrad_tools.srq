from rf2.devices.dg4xxx import DG4xxx, DG4xxxProxy

class Device(DG4xxx):
    _amplitude_range = (0.0, 5.0)
    _amplitude_units = 'V'
    _frequency_range = (0, 160e6)
    _source = 1
    _vxi11_address = '192.168.1.40'

class DeviceProxy(Device, DG4xxxProxy):
    _vxi11_servername = 'yesr10_vxi11'
    
    def __init__(self, cxn=None, **kwargs):
        DG4xxxProxy.__init__(self, cxn=cxn, **kwargs)
