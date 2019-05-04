from pressure_gauge.devices import kjl375

class Device(kjl375.KJL375):
    _serial_port = 'COM8'

class DeviceProxy(Device, kjl375.KJL375Proxy):
    _serial_servername = 'yesr3_serial'
    
    def __init__(self, **kwargs):
        kjl375.KJL375Proxy.__init__(self, **kwargs)
