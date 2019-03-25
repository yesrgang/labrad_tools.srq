from current_controller3.devices.ldc80 import LDC80, LDC80Proxy

class Device(LDC80):
    autostart = False
    gpib_address = 'GPIB0::9::INSTR'

    pro8_slot = 2
    default_current = 0.1500
    current_range = [0.0, 0.155]

class DeviceProxy(Device, LDC80Proxy):
    gpib_servername = 'yesr20_visa2'
