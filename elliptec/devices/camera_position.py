from elliptec.devices.ell7 import ELL7, ELL7Proxy

class Device(ELL7):
#    serial_port = '/dev/ttyUSB04036015'
    serial_port = '/dev/ttyUSB04036015DM00YKEC'
    address = 0
    
class DeviceProxy(Device, ELL7Proxy):
    serial_servername = 'yesr10_serial'
