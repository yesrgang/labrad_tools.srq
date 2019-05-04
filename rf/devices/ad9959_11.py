import rf.devices.ad9959.device 
reload(rf.devices.ad9959.device)
from rf.devices.ad9959.device import AD9959

class Channel(AD9959):
    autostart = False
    serial_servername = "yesr5_serial"
    serial_address = "COM24"
    board_num = 0
    channel = 3

    default_frequency = 122e6
    default_amplitude = 0.76

Device = Channel
