from rf.devices.ad9854.device import AD9854

class AOM(AD9854):
    autostart = True
    serial_servername = "yesr10_serial"
    serial_address = "/dev/ttyACM649383339323514011E0"
    subaddress = 5

    default_frequency = 80.0e6

Device = AOM
