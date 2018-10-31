from current_controller.devices.verdi.device import Verdi

class M2Verdi(Verdi):
    autostart = False
    serial_servername = 'yesr20_serial'
    serial_address = 'COM19'

    power_range = (0.0, 18.0) # [W]

    default_power = 18.0 # [W]

Device = M2Verdi
