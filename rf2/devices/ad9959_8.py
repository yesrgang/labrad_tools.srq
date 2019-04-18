from rf2.devices.ad9959 import AD9959, AD9959Proxy

class Device(AD9959):
    _serial_port = 'COM24'
    _arduino_address = 0
    _channel_num = 0

    def _setup(self):
        self.amplitude = 1
        self.frequency = 122e6
#        self.sweep = 'amplitude'

class DeviceProxy(Device, AD9959Proxy):
    _serial_servername = 'yesr5_serial'

    def __init__(self, **kwargs):
        AD9959Proxy.__init__(self, **kwargs)
