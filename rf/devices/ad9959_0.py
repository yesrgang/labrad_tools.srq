from rf.devices.ad9959.device import AD9959

class Channel(AD9959):
    autostart = False
    serial_servername = "yesr10_serial"
    serial_address = "/dev/ttyACM853323434323510101E0"
    board_num = 0
    channel = 0

    default_frequency = 0e6

Device = Channel
