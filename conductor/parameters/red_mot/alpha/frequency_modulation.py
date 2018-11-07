import json

import vxi11

from conductor.parameter import ConductorParameter


class FrequencyModulation(ConductorParameter):
    priority = 1
    autostart = True
    call_in_thread = True
    awg_devicename = 'alpha_fm'
    waveforms = {
        'red_mot': 'INT:\\ALPHA.ARB',
        'rm_tof': 'INT:\\ALPHA.ARB',
        'red_mot-fast': 'INT:\\ALPHA_FAST.ARB',
        'red_mot-fast-tof': 'INT:\\ALPHA_FAST.ARB',
        }

    def initialize(self, config):
        super(FrequencyModulation, self).initialize(config)
        self.connect_to_labrad()
    
    def update(self):
        sequence = self.server._get_parameter_value('sequencer.sequence')

        for subsequence, waveform in self.waveforms.items():
            if subsequence in sequence:
                request = {self.awg_devicename: waveform}
                self.cxn.awg.waveforms(json.dumps(request))

Parameter = FrequencyModulation
