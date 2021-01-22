from conductor.parameter import ConductorParameter

class MJMCombDemodFrequency(ConductorParameter):
    priority = 1
    autostart = False
    def initialize(self, config):
        super(MJMCombDemodFrequency, self).initialize(config)
        self.connect_to_labrad()

    def update(self):
        self.value = self.cxn.si_demod.get_frequency()

Parameter = MJMCombDemodFrequency
