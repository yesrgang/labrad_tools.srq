from current_controller.devices.ldc80xx.device import Ldc80xx

class Blue2D(Ldc80xx):
    autostart = False
    gpib_servername = 'yesr20_visa'
    gpib_address = 'GPIB0::9::INSTR'

    pro8_slot = 4
    default_current = 0.1501

Device = Blue2D
