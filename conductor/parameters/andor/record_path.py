import json
import numpy as np
import time

from conductor.parameter import ConductorParameter


class RecordPath(ConductorParameter):
    autostart = False
    priority = 2
    record_sequences = {
        'image': 'record_g',
        'image_3P1_excitation': 'record_g',
        'image_3P1_excitation-405': 'record_g',
        'image_v2': 'record_g',
        'image_clock': 'record_eg',
        'image_ft': 'record_eg',
        }

    data_filename = '{}.ikon'
    nondata_filename = '{}/ikon'

    image_settings = {}

    def initialize(self, config):
        print 'initing andor.record_path'
        super(RecordPath, self).initialize(config)
        self.connect_to_labrad()
        self.cxn.yesr10_andor.select_device('hr_ikon')
    
    @property
    def value(self):
        experiment_name = self.server.experiment.get('name')
        shot_number = self.server.experiment.get('shot_number')
        sequence = self.server.parameters.get('sequencer.sequence')
        previous_sequence = self.server.parameters.get('sequencer.previous_sequence')

        value = None
        rel_point_path = None
        self.recorder_name = None
        if (experiment_name is not None) and (sequence is not None):
            point_filename = self.data_filename.format(shot_number)
            rel_point_path = os.path.join(experiment_name, point_filename)
        elif sequence is not None:
            rel_point_path = self.nondata_filename.format(time.strftime('%Y%m%d'))

        
        if sequence.loop:
            if np.intersect1d(previous_sequence.value, self.record_sequences.keys()):
                intersection = np.intersect1d(previous_sequence.value, self.record_sequences.keys())
                value = rel_point_path
                self.recorder_name = self.record_sequences[intersection[-1]]
        elif np.intersect1d(sequence.value, self.record_sequences.keys()):
            intersection = np.intersect1d(sequence.value, self.record_sequences.keys())
            value = rel_point_path
            self.recorder_name = self.record_sequences[intersection[-1]]

        return value
    
    @value.setter
    def value(self, x):
        pass
    
    def update(self):
        if self.value is not None:
            print self.value
            image_settings_json = json.dumps(self.image_settings)
            self.cxn.yesr10_andor.record(self.value, self.recorder_name, image_settings_json)
        else:
            print self.nondata_filename
#        experiment_name = self.server.experiment.get('name')
#        shot_number = self.server.experiment.get('shot_number')
#
#        
#        pt_filename = self.data_filename.format(exp_pt)
#        pt_path = run_dir + pt_filename
#        
#        recorder_type = ''
#        try:
#            sequence = self.conductor.parameters['sequencer']['sequence'].value
#            for subsequence in self.recorders:
#                if subsequence in sequence:
#                    recorder_type = self.recorders[subsequence]
#        except:
#            print "conductor's andor ikon unable to determine sequence"
#
#        if recorder_type:
#            image_settings_json = json.dumps(self.image_settings)
#            yield self.cxn.yesr10_andor.record(pt_path, recorder_type, image_settings_json)

Parameter = RecordPath
