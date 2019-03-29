import numpy as np

from conductor.parameter import ConductorParameter
from elliptec.devices.camera_position import DeviceProxy

class Position(ConductorParameter, DeviceProxy):
    priority = 1
    sequence_positions = {
        'image': 2.8,
        'image-red': 18,
        'image-red-sigma': 18,
        'image-red-sigma-osg': 18,
        'image-red-sigma-osg-m': 18,
        'image-osg2-red': 18,
        'image-osg2-red-m': 18,
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
