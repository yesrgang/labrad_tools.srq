from rf2.devices.e44xx import E44xx, E44xxProxy


class Device(E44xx):
    _amplitude_range = (-20, 20)
    _amplitude_units = 'dBm'
    _frequency_range = (250e3, 3e9)
    _visa_address = 'GPIB0::19::INSTR'

class DeviceProxy(Device, E44xxProxy):
    _visa_servername = 'yesr9_visa2'
    
    def __init__(self, cxn=None, **kwargs):
        E44xxProxy.__init__(self, cxn=cxn, **kwargs)
