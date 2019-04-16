from current_controller3.devices.ldc50 import LDC50

class Device(LDC50):
    socket_address = ('192.168.1.41', 8888)
    _current_range = (0.0, 0.155)
    _relock_stepsize = 0.002
    _locked_threshold = 160e-3

class DeviceProxy(Device, LDC50):
    def __init__(self, cxn, **kwargs):
        LDC50.__init__(self, **kwargs)
