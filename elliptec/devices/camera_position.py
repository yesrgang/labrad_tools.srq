from elliptec.devices.ello import ELLO, ELLOProxy

class Device(ELLO):
#    serial_port = '/dev/ttyUSB04036015'
    serial_port = '/dev/ttyUSB04036015DM00YKEC'
    address = 0
    
class DeviceProxy(Device, ELLOProxy):
    serial_servername = 'yesr10_serial'
