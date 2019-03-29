from rf2.devices.dg4 import DG4

class Device(DG4):
    vxi11_address = '192.168.1.40'
    source = 2

    frequency_range = (0, 160e6)
    amplitude_range = (0.0, 5.0)
    amplitude_units = 'V'
    offset_range = (-10, 10)
