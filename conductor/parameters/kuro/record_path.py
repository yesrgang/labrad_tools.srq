import numpy as np
import os
import time

from conductor.parameter import ConductorParameter

class Parameter(ConductorParameter):
    autostart = True
    priority = 1
#    call_in_thread = True
    
#    data_filename = '/home/srgang/srqdata/data/{}/{}.kuro.hdf5'
#    nondata_filename = '/home/srgang/srqdata/data/{}/kuro.hdf5'
#    watchdir = '/home/srgang/srqdata/data/kuro-tmp-images/'
    data_filename = 'Q:\\data\\{}\\{}.kuro.hdf5'
    nondata_filename = 'Q:\\data\\{}\\kuro.hdf5'
    watchdir = '/srqdata2/data/kuro-tmp-images/'

    data_directory = os.path.join(os.getenv('PROJECT_DATA_PATH'), 'data')
    
    def initialize(self, config):
        super(Parameter, self).initialize(config)
    
    @property
    def value(self):
        experiment_name = self.server.experiment.get('name')
        shot_number = self.server.experiment.get('shot_number')

        rel_point_path = None
        if (experiment_name is not None):
            return self.data_filename.format(experiment_name, shot_number)
        else:
            return self.nondata_filename.format(time.strftime('%Y%m%d'))
        

    def update(self):
        sequence = self.server.parameters.get('sequencer.sequence')
        previous_sequence = self.server.parameters.get('sequencer.previous_sequence')
        sequence_value = None

        if sequence.loop:
            sequence_value = previous_sequence.value
        else:
            sequence_value = sequence.value

        for sub_sequence in sequence_value:
            if 'princeton' in sub_sequence:
                with open(os.path.join(self.watchdir, 'destination.txt'), 'w') as f:
                    f.write(self.value)
