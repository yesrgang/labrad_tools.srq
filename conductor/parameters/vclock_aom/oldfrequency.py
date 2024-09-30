import json

from conductor.parameter import ConductorParameter

class Frequency(ConductorParameter):
    autostart = False
    #priority = 2
    priority = 12


    def initialize(self, config):
        super(Frequency, self).initialize(config)
        self.connect_to_labrad()
    
    def update(self):
        if self.value is not None:
            request =  {
                'clock_steer2': self.value
                }
            self.cxn.rf.frequencies(json.dumps(request))

Parameter = Frequency
