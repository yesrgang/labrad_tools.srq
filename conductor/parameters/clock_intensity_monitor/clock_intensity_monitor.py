import json
import numpy as np
import time
import os

from conductor.parameter import ConductorParameter

class Parameter(ConductorParameter):
    autostart = True
    priority = 1
    call_in_thread = True

    record_types = [
            'rabi-clock',
            'rabi-clock-x',
            'ramsey-dark',
            'rabi-clock-cleanup',
            'rabi-clock-x-CLKINTOLL',
            ]
    
    
    data_filename = 'Q:/data/{}/{}.pico.npz'
    nondata_filename = 'Q:/data/{}/pico.npz'

    def initialize(self, config):
        self.connect_to_labrad()

    
    @property
    def value(self):
        experiment_name = self.server.experiment.get('name')
        shot_number = self.server.experiment.get('shot_number')

        if (experiment_name is not None):
            return self.data_filename.format(experiment_name, shot_number)
        else:
            return self.nondata_filename.format(time.strftime('%Y%m%d'))

    def update(self):
        sequence = self.server.parameters.get('sequencer.sequence')
        previous_sequence = self.server.parameters.get('sequencer.previous_sequence')
        record_type = None
        sequence_value = None

        if sequence.loop:
            sequence_value = previous_sequence.value
        else:
            sequence_value = sequence.value
#        print(sequence.value)
        intersection = np.intersect1d(sequence_value, self.record_types)

        # get picoscope record parameters
        model = self.server.parameters.get('sequencer.pico-model')
        serial_no = self.server.parameters.get('sequencer.pico-serialno')
        duration = self.server.parameters.get('sequencer.pico-duration')
        presamples = self.server.parameters.get('sequencer.pico-presamples')
        postsamples = self.server.parameters.get('sequencer.pico-postsamples')

        if len(intersection) > 0:
            try:
                if model.value == 5000:
                    self.cxn.yesr13_picoscope.set_recordduration_5000a(duration.value,presamples.value,postsamples.value)
                    self.cxn.yesr13_picoscope.get_data_5000a(self.value,serial_no.value)
                elif model.value == 3000:
                    self.cxn.yesr13_picoscope.set_recordduration_3000a(duration.value,presamples.value,postsamples.value)
                    self.cxn.yesr13_picoscope.get_data_3000a(self.value,serial_no.value)

            except Exception as e:
                print('yesr13_picoscope error! Check conductor parameter and enable error output in "clock_intensity_monitor" for details')
                print(e)
            
