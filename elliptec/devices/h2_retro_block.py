from elliptec.devices.ell6 import ELL6, ELL6Proxy

class Device(ELL6):
    serial_port = '/dev/ttyUSB04036015DM014TC7'
    address = 0
   
    @property
    def blocked(self):
        if self.position:
            return True
        else:
            return False

    @blocked.setter
    def blocked(self, blocked):
        if blocked:
            self.position = 1
        else:
            self.position = 0
    
class DeviceProxy(Device, ELL6Proxy):
    serial_servername = 'yesr10_serial'
