from current_controller.devices.ldc80xx.device import Ldc80xx

class BlueZS(Ldc80xx):
    autostart = False
    gpib_servername = 'yesr20_visa'
    gpib_address = 'GPIB0::9::INSTR'

    pro8_slot = 6
    default_current = 0.1500

Device = BlueZS
