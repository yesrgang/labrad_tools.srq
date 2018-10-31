from rf.devices.hp_signal_generator.device import HPSignalGenerator


class Alpha(HPSignalGenerator):
    autostart = True
    visa_servername = 'yesr9_visa'
    visa_address = 'GPIB0::19::INSTR'

    frequency_range = (250e3, 3e9)
    amplitude_range = (-20, 20)

    def initialize(self, config):
        super(Alpha, self).initialize(config)
        self.rm.write('FM1:DEV 2e6')
        self.set_amplitude(10)
        self.set_state(True)

Device = Alpha
