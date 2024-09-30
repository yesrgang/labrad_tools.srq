import json

import vxi11

from conductor.parameter import ConductorParameter


class FrequencyModulation(ConductorParameter):
    priority = 1
    autostart = False
    call_in_thread = True
    awg_devicename = 'alpha_fm'
    waveforms = {
        'red-mot': 'INT:\\ALPHA.ARB',
        'red-mot-tof': 'INT:\\ALPHA.ARB',
        'red-mot-fast': 'INT:\\ALPHA_FAST.ARB',
        'red-mot-fast-tof': 'INT:\\ALPHA_FAST.ARB',
        }

    def initialize(self, config):
        super(FrequencyModulation, self).initialize(config)
        self.connect_to_labrad()
        request = {self.awg_devicename: 'INT:\\ALPHA.ARB'}
        self.cxn.awg.waveforms(json.dumps(request))
        self.cxn.awg.amplitude('alpha_fm', 0.225)
    
    def update(self):
        sequence = self.server._get_parameter_value('sequencer.sequence')

        for subsequence, waveform in self.waveforms.items():
            if subsequence in sequence:
                request = {self.awg_devicename: waveform}
                self.cxn.awg.waveforms(json.dumps(request))

Parameter = FrequencyModulation
