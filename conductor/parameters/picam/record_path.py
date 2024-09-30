import json
import numpy as np
import time
import os

from conductor.parameter import ConductorParameter

class Parameter(ConductorParameter):
    autostart = False
    priority = 1
#    call_in_thread = True
    record_types = {
        "image-princeton": "absorption",
        "image-princeton-tmp": "absorption",
        "image-princeton-slow": "absorption",
        "image-princeton-slow-tmp": "absorption",
        "image-princeton-tens4": "absorption",
        "image-princeton-tens4-slow": "absorption",
        "image-princeton-single": "absorption",
        "image-princeton-single-slow": "absorption",
        "image-princeton-single-odt": "absorption",
        "image-princeton-lat": "fluorescence",
        "image-princeton-lat-slow": "absorption",
        "image-princeton-lat-slow-tmp": "absorption",
        "image-princeton-lat-single": "single",
        "image-princeton-lat-bmap": "absorption",
        "image-princeton-kill": "fluorescence",
        "image-lat": "absorption",
        "image-princeton-pco": "fluorescence",
        }

    data_filename = 'Q:\\data\\{}\\{}.kuro.hdf5'
    nondata_filename = 'Q:\\data\\{}\\kuro.hdf5'

    data_directory = os.path.join(os.getenv('PROJECT_DATA_PATH'), 'data')

    
    def initialize(self, config):
        super(Parameter, self).initialize(config)
        self.connect_to_labrad() # gives us self.cxn
    
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

        if record_type == 'absorption':
            self.cxn.yesr20_picam.acquire(self.value)

