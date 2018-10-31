from power_supply.devices.psh6018.device import PSH6018

class QuadrantCoils(PSH6018):
    autostart = False
    serial_servername = 'yesr10_serial'
    serial_address = '/dev/ttyUSB0'

Device = QuadrantCoils
