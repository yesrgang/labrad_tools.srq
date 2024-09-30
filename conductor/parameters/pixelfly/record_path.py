import json
import numpy as np
import time
import os

from conductor.parameter import ConductorParameter

class Parameter(ConductorParameter):
    autostart = True
    priority = 1
    call_in_thread = True
    record_types = {
        "image-odt-pco": "absorption",
        "image-rm-pco": "absorption",
        "image-pco": "absorption",
        "image-odt": "absorption",
        "image-lattice": "absorption",
        "image-odt-lattice": "absorption",
        "image": "absorption",
        "image-tmp": "absorption",
#        "image-princeton": "absorption",
        "image-princeton-pco": "absorption",
        "image-princeton-pco-odt": "absorption",
        "image-odt-tens4": "absorption",
#        "image-princeton-single": "absorption",
#        "image-princeton-single-repump": "fluorescence",

        }

    data_filename = 'Q:\\data\\{}\\{}.pixelfly.hdf5'
    nondata_filename = 'Q:\\data\\{}\\pixelfly.hdf5'

    data_directory = os.path.join(os.getenv('PROJECT_DATA_PATH'), 'data')

    
    def initialize(self, config):
        super(Parameter, self).initialize(config)
        self.connect_to_labrad()
        print('pixelfly ready!')

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
#        try:
#            record_type = self.record_types.get(intersection[-1])
#        except:
#            pass
    
        if record_type == 'absorption':
            self.cxn.yesr13_pixelfly.take_picture(self.value)

#        if record_type == 'fluorescence':
#            self.cxn.yesr13_pixelfly.take_picture_fl(self.value)
