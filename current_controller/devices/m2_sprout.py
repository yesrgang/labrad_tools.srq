from current_controller.devices.sprout.device import Sprout

class M2Sprout(Sprout):
    autostart = False
    serial_servername = 'yesr5_serial'
    serial_address = 'COM9'

Device = M2Sprout
