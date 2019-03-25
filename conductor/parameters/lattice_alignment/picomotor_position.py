import json

from conductor.parameter import ConductorParameter

class PicomotorPosition(ConductorParameter):
    priority = 1
    picomotor_name = None
    call_in_thread = False

    def initialize(self, config):
        print '{} initd'.format(self.name)
        super(PicomotorPosition, self).initialize(config)
        self.connect_to_labrad()
    
    def update(self):
        if (self.value is not None):
            request = {self.picomotor_name: self.value}
            self.cxn.picomotor.positions(json.dumps(request))
            if type(self.value).__name__ is not 'list':
                self.value = None
