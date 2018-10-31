from stepper_motor.devices.silver_pack17.device import SilverPack17

class NdFilter(SilverPack17):
    enabled = True
    serial_servername = 'yesr20_serial'
    serial_address = 'COM11'

Device = NdFilter
