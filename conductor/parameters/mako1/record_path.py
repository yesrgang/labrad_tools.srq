import numpy as np
import os
import time

from conductor.parameter import ConductorParameter

class Parameter(ConductorParameter):
    autostart = False
    priority = 1
    call_in_thread = False
    record_types = {
        "image": "normal",
        "image-odt": "normal",
        "image-odt-tmp": "normal",
        "image-odt-tens4": "normal",
        "image-odt-tens4-tmp": "normal",
        }

    data_filename = '/home/srgang/srqdata/data/{}/{}.mako1.hdf5'
    nondata_filename = '/home/srgang/srqdata/data/{}/mako1.hdf5'

    data_directory = os.path.join(os.getenv('PROJECT_DATA_PATH'), 'data')

    
    def initialize(self, config):
        super(Parameter, self).initialize(config)
        self.connect_to_labrad() # gives us self.cxn
        self.cxn.yesr10_vimba.arm_mako1()
    
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
        record_type = None
        sequence_value = None

        if sequence.loop:
            sequence_value = previous_sequence.value
        else:
            sequence_value = sequence.value
        intersection = np.intersect1d(sequence_value, self.record_types.keys())
        if intersection:
            record_type = self.record_types.get(intersection[-1])
        
        if record_type == 'normal':
            self.cxn.yesr10_vimba.get_frames_mako1(self.value)
