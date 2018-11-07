from ecdl.devices.aosense_ecdl.device import AOSenseECDL

class BlueMaster(AOSenseECDL):
    autostart = False
    serial_servername = 'yesr20_serial'
    serial_address = 'COM12'

    default_diode_current = 126.0 # [mA]

Device = BlueMaster
