import json

from conductor.parameter import ConductorParameter

class DemodFrequency(ConductorParameter):
    autostart = False
    #priority = 2
    priority = 12
    value = 135e6

    dark_offset = 1e6
    ramp_rate = 10

    def initialize(self, config):
        super(DemodFrequency, self).initialize(config)
        self.connect_to_labrad()
    
    def update(self):
        if self.value is not None:
            min_freq = min([abs(self.value), abs(self.value + self.dark_offset)])
            max_freq = max([abs(self.value), abs(self.value + self.dark_offset)])
            request =  {
                'ad9959_3': {
                    'start': min_freq, 
                    'stop': max_freq, 
                    'rate': self.ramp_rate
                    } 
                }
            self.cxn.rf.linear_ramps(json.dumps(request))

Parameter = DemodFrequency
