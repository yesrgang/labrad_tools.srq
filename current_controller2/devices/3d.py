from current_controller.devices.ldc80xx.device import Ldc80xx

class Blue3D(Ldc80xx):
    autostart = False
    gpib_servername = 'yesr20_visa'
    gpib_address = 'GPIB0::9::INSTR'

    pro8_slot = 2
    default_current = 0.1498

Device = Blue3D
