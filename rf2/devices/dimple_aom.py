from rf2.devices.ad9854 import AD9854, AD9854Proxy

class Device(AD9854):
    _serial_port = '/dev/ttyACM649383339323514011E0'
    _arduino_address = 5

    def _setup(self):
        self.amplitude = 1.0
        self.frequency = 80e6

class DeviceProxy(Device, AD9854Proxy):
    _serial_servername = 'yesr10_serial'

    def __init__(self, **kwargs):
        AD9854Proxy.__init__(self, **kwargs)
