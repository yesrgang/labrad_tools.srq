from ecdl2.devices.aosense_ecdl import AOSenseECDL, AOSenseECDLProxy

class Device(AOSenseECDL):
    _serial_address = 'COM12'
    _default_diode_current = 126.0 # [mA]

class DeviceProxy(Device, AOSenseECDLProxy):
    _serial_servername = 'yesr20_serial'

    def __init__(self, cxn=None, **kwargs):
        AOSenseECDLProxy.__init__(self, cxn, **kwargs)
