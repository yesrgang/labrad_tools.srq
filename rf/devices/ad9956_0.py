from rf.devices.ad9956.device import AD9956

class Channel(AD9956):
    autostart = False
    serial_servername = "yesr10_serial"
    serial_address = "/dev/ttyACM85332343432351F0E180"
    board_num = 0
    channel = 0

    default_frequency = 0e6

Device = Channel
