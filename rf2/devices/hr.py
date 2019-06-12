from rf2.devices.ad9959 import AD9959, AD9959Proxy

class Device(AD9959):
    _serial_port = '/dev/ttyACM9573632363235180F022'
    _arduino_address = 1
    _channel_num = 2

    def _setup(self):
        self.amplitude = 0.6
        self.frequency = 80.2e6
        self.sweep = 'amplitude'

class DeviceProxy(Device, AD9959Proxy):
    _serial_servername = 'yesr10_serial'
    
    def __init__(self, **kwargs):
        AD9959Proxy.__init__(self, **kwargs)
