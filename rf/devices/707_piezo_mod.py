from rf.devices.dg1000z.device import DG1000Z

class PiezoMod707(DG1000Z):
    vxi11_address = '192.168.1.19'
    source = 1

    frequency_range = (1e-6, 5e3)
    amplitude_range = (0.0, 5.0)
    amplitude_units = 'V'
    offset_range = (-10, 10)

    update_parameters = ['state', 'offset']

    def initialize(self, config):
        pass
#        DG1000Z.initialize(self, config)
#        self.vxi11.write('SOUR1:FREQ 5.5e2')
#        self.vxi11.write('SOUR1:VOLT 3')
#        self.vxi11.write('SOUR1:VOLT:OFFS 0')
#        self.vxi11.write('SOUR1:FUNC:RAMP:SYMM 50')
#        self.vxi11.write('SOUR1:APPL:RAMP')
#        self.vxi11.write('OUTP1:LOAD INF')
#        self.vxi11.write('OUTP1:STAT 1')

Device = PiezoMod707
