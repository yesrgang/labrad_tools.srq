import json

import vxi11

from conductor.parameter import ConductorParameter


class FrequencyModulation(ConductorParameter):
    priority = 1
    autostart = True
    call_in_thread = True
    awg_devicename = 'beta_fm'
    waveforms = {
        'red_mot': 'INT:\\BETA.ARB',
        'rm_tof': 'INT:\\BETA.ARB',
        'red_mot-fast': 'INT:\\BETA_FAST.ARB',
        'red_mot-fast-tof': 'INT:\\BETA_FAST.ARB',
        }

    def initialize(self, config):
        super(FrequencyModulation, self).initialize(config)
        self.connect_to_labrad()
    
    def update(self):
        sequence = self.server._get_parameter_value('sequencer.sequence')

        for subsequence, waveform in self.waveforms.items():
            if subsequence in sequence:
                if waveform != self.value:
                    request = {self.awg_devicename: waveform}
                    self.cxn.awg.waveforms(json.dumps(request))
                    self.value = waveform

Parameter = FrequencyModulation
