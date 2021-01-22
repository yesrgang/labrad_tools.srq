from ecdl2.devices.aosense_ecdl import AOSenseECDL, AOSenseECDLProxy

class Device(AOSenseECDL):
    _serial_address = '/dev/ttyUSBAOS102717-07'
#    _serial_address = '/dev/ttyUSB0'
#    _serial_address = 'COM3'
    _diode_current_range = (10.0, 95.0)

class DeviceProxy(Device, AOSenseECDLProxy):
    _serial_servername = 'yesr9_serial'
#    _serial_servername = 'm2_serial'

    def __init__(self, cxn=None, **kwargs):
        AOSenseECDLProxy.__init__(self, cxn, **kwargs)
