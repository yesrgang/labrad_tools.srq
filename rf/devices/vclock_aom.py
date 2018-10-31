from rf.devices.dg1000z.device import DG1000Z

class VClockAOM(DG1000Z):
    vxi11_address = '192.168.1.5'
    source = 1

    frequency_range = (50e3, 60e6)
    amplitude_range = (0.0, 1.5)
    default_amplitude = 1.5

    def initialize(self):
        DG1000Z.initialize(self)
        self.set_amplitude(self.default_amplitude)
        self.vxi11.write('OUTP1:LOAD 50')
        self.vxi11.write('SOUR1:VOLT:OFFS 0')
        self.vxi11.write('OUTP1:STAT 1')

Device = VClockAOM
