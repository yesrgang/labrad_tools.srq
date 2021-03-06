import numpy as np

from conductor.parameter import ConductorParameter
from elliptec.devices.camera_position import DeviceProxy

class Position(ConductorParameter, DeviceProxy):
    priority = 1
    sequence_positions = {
#        'image': 3.0, #2.8
        'image': 24.5, # now objective
        'image-red': 18.2, #18.0
        'image-red-sigma': 18.2, #18.4
        'image-red-sigma-osg': 18.2,
        'image-red-sigma-osg-m': 18.2,
        'image-osg2-red': 18.2,
        'image-osg2-red-m': 18.2,
        'image-clock-superradiance': 18.2,
        'image-clock-superradiance_689': 18.2,
        }
    autostart = True
    
    def update(self):
        sequence = self.server.parameters.get('sequencer.sequence')
        previous_sequence = self.server.parameters.get('sequencer.previous_sequence')
        
        previous_value = self.value
        if sequence.loop:
            intersection = np.intersect1d(previous_sequence.value, self.sequence_positions.keys())
        else:
            intersection = np.intersect1d(sequence.value, self.sequence_positions.keys())
        if intersection:
            self.value = self.sequence_positions[intersection[-1]]
                
        if self.value != previous_value:
            self.position = self.value
        

Parameter = Position
