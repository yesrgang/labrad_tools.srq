from current_controller3.devices.ldc50 import LDC50

class _3D3(LDC50):
    socket_address = ('192.168.1.41', 8888)
    _relock_stepsize = 0.002
