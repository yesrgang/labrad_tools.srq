from rf2.devices.ad9959 import AD9959, AD9959Proxy

class Device(AD9959):
    serial_port = 'COM24'
    arduino_address = 0
    channel_number = 1
    
    default_amplitude = 1
    default_frequency = 122e6
    default_sweep = 'amplitude'

    def __init__(self, **kwargs):
        AD9959.__init__(self, **kwargs)
        self.amplitude = self.default_amplitude
        self.frequency = self.default_frequency
        self.sweep = self.default_sweep

class DeviceProxy(Device, AD9959Proxy):
    serial_servername = 'yesr5_serial'

    def __init__(self, **kwargs):
        AD9959Proxy.__init__(self, **kwargs)
        self.amplitude = self.default_amplitude
        self.frequency = self.default_frequency
        self.sweep = self.default_sweep
