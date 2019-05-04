from rf.devices.ad9959.device import AD9959

class Channel(AD9959):
    autostart = False
    serial_servername = "yesr5_serial"
    serial_address = "COM24"
    board_num = 1
    channel = 1

    default_frequency = 0e6

Device = Channel
