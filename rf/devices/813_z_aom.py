from rf.devices.ad9854.device import AD9854

class AOM(AD9854):
    autostart = True
    serial_servername = "yesr10_serial"
    serial_address = "/dev/ttyACM649383339323514011E0"
    subaddress = 2

    default_frequency = 125e6
    default_amplitude = 1

Device = AOM
