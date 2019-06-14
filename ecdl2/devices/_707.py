from ecdl2.devices.aosense_ecdl import AOSenseECDL, AOSenseECDLProxy

class Device(AOSenseECDL):
#    _serial_address = '/dev/ttyUSB1'
    _serial_address = 'COM4'
    _diode_current_range = (10.0, 95.0)

class DeviceProxy(Device, AOSenseECDLProxy):
#    _serial_servername = 'yesr9_serial'
    _serial_servername = 'm2_serial'

    def __init__(self, cxn=None, **kwargs):
        AOSenseECDLProxy.__init__(self, cxn, **kwargs)
