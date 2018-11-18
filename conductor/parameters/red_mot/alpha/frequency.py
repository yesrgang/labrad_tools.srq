import json

from conductor.parameter import ConductorParameter


class Frequency(ConductorParameter):
    priority = 1
    autostart = True
    call_in_thread = True
    rf_devicename = 'alpha'

    def initialize(self, config):
        super(Frequency, self).initialize(config)
        self.connect_to_labrad()
    
    def update(self):
        request = {self.rf_devicename: None}
        response_json = self.cxn.rf.frequencies(json.dumps(request))
        self.value = json.loads(response_json)

Parameter = Frequency
