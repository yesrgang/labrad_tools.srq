from ecdl2.devices.aosense_ecdl import AOSenseECDL, AOSenseECDLProxy

class Device(AOSenseECDL):
    _serial_address = 'COM5'
    _default_diode_current = 130.99 # [mA]

class DeviceProxy(Device, AOSenseECDLProxy):
    _serial_servername = 'yesr8_serial'

    def __init__(self, cxn=None, **kwargs):
        AOSenseECDLProxy.__init__(self, cxn, **kwargs)
