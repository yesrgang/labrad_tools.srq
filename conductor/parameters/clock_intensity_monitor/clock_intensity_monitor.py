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
            'rabi-clock-cleanup'
            ]
    
    
    data_filename = 'Q:/data/{}/{}.pico.hdf5'
    nondata_filename = 'Q:/data/{}/pico.hdf5'

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
        if len(intersection) > 0:
            self.cxn.yesr13_picoscope.get_data(self.value)
            
