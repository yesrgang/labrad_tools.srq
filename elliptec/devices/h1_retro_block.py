from elliptec.devices.ell6 import ELL6, ELL6Proxy

class Device(ELL6):
    serial_port = '/dev/ttyUSB04036015DM00YKOI'
    address = 0

    @property
    def blocked(self):
        if self.position:
            return False
        else:
            return True

    @blocked.setter
    def blocked(self, blocked):
        if blocked:
            self.position = 0
        else:
            self.position = 1
    
class DeviceProxy(Device, ELL6Proxy):
    serial_servername = 'yesr10_serial'
