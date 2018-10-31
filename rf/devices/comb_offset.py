from rf.devices.mfg2160.device import MFG2160

class CombOffset(MFG2160):
    serial_servername = 'yesr5_serial'
    serial_address = "COM14"

    frequency_range = (10e6, 300e6)
    amplitude_range = (0, 1)
    
    def initialize(self):
        MFG2160.initialize(self)
        self.serial_server.write_line(self.serial_address, 'SOUR3RF:AMP MAX')

Device = CombOffset
