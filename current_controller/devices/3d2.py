from current_controller.devices.ldc80xx.device import Ldc80xx

class MOT2(Ldc80xx):
    autostart = False
    gpib_servername = 'yesr20_visa'
    gpib_address = 'GPIB0::9::INSTR'

    pro8_slot = 8
    default_current = 0.1500 # [A]

Device = MOT2
