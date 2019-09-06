from current_controller3.devices.ldc80 import LDC80, LDC80Proxy

class Device(LDC80):
    _current_range = (0.0, 0.155)
    _visa_address = 'GPIB0::9::INSTR'
    _locked_threshold = 7.1e-3
    _pro8_slot = 8
    _relock_stepsize = 0.002

class DeviceProxy(Device, LDC80Proxy):
    _visa_servername = 'yesr20_visa2'
