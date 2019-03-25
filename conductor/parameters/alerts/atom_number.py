import json

from conductor.parameter import ConductorParameter

class AtomNumber(ConductorParameter):
    """ value set by sequencer.sequence """ 
    autostart = False
    priority = 1
    call_in_thread = True

    def initialize(self, config):
        super(AtomNumber, self).initialize(config)
        self.connect_to_labrad()

    def update(self):
        request = {'blue_pmt': -1}
        response_json = self.cxn.pmt.retrive_records(json.dumps(request))
        response = json.loads(response_json)
        if response['blue_pmt']['tot_sum'] < 8000:
            self.cxn.beeper.beep()



Parameter = AtomNumber
