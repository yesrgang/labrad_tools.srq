import json
import numpy as np
import time
import os
import h5py

from conductor.parameter import ConductorParameter

from andor_server.proxy import AndorProxy

class RecordPath(ConductorParameter):
    autostart = False
    priority = 1
    record_types = {
        "image": "absorption",
        }

    data_filename = '{}.ikon.hdf5'
    nondata_filename = '{}/ikon.hdf5'

    data_directory = os.path.join(os.getenv('PROJECT_DATA_PATH'), 'data')
    compression = 'gzip'
    compression_level = 4

    def initialize(self, config):
        super(RecordPath, self).initialize(config)
        self.connect_to_labrad()
        andor = AndorProxy(self.cxn.yesr10_andor)
        andor.Initialize()
        andor.SetFanMode(2)
        andor.SetTemperature(-70)
        andor.SetCoolerMode(0)
        andor.CoolerON()
        self._andor = andor
    
    @property
    def value(self):
        experiment_name = self.server.experiment.get('name')
        shot_number = self.server.experiment.get('shot_number')

        rel_point_path = None
        if (experiment_name is not None):
            point_filename = self.data_filename.format(shot_number)
            return os.path.join(experiment_name, point_filename)
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
        record_type = self.record_types.get(intersection[-1])
    
        print 'rt', record_type
        if record_type == 'absorption':
            self.take_absorption_image()
        self.server._send_update({self.name: self.value})
        

    def take_absorption_image(self):
        andor = self._andor
        
        andor.AbortAcquisition()
        andor.SetAcquisitionMode(3)
        andor.SetReadMode(4)
        andor.SetNumberAccumulations(1)
        andor.SetNumberKinetics(2)
        andor.SetAccumulationCycleTime(0)
        andor.SetKineticCycleTime(0)
        andor.SetPreAmpGain(0)
        andor.SetHSSpeed(0, 0)
        andor.SetVSSpeed(1)
        andor.SetShutter(1, 1, 0, 0)
        andor.SetTriggerMode(1)
        andor.SetExposureTime(500e-6)
        andor.SetImage(1, 1, 1, 1024, 1, 1024)
        
        for i in range(2):
            andor.StartAcquisition()
            andor.WaitForAcquisition()

        data = andor.GetAcquiredData(2 * 1024 * 1024).reshape(2, 1024, 1024)
        images = {key: data[i] 
                  for i, key in enumerate(["image", "bright"])}
        
        data_path = os.path.join(self.data_directory, self.value)
        data_directory = os.path.dirname(data_path)
        if not os.path.isdir(data_directory):
            os.makedirs(data_directory)

        h5f = h5py.File(data_path, "w")
        for image in images:
            h5f.create_dataset(image, data=images[image], 
                    compression=self.compression, 
                    compression_opts=self.compression_level)
        h5f.close()

        print data_path

Parameter = RecordPath
