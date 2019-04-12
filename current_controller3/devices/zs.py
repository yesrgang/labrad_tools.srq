from current_controller3.devices.ldc80 import LDC80, LDC80Proxy

class Device(LDC80):
    _current_range = (0.0, 0.155)
    _gpib_address = 'GPIB0::9::INSTR'
    _locked_threshold = 11.9e-3
    _pro8_slot = 6
    _relock_stepsize = 0.001

class DeviceProxy(Device, LDC80Proxy):
    _gpib_servername = 'yesr20_visa2'
