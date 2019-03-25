import numpy as np

from conductor.parameter import ConductorParameter
from elliptec.devices.camera_position import DeviceProxy

class Position(ConductorParameter, DeviceProxy):
    priority = 1
    sequence_positions = {
        'image': 2.8,
        'image-red': 18.7,
        'image-red-sigma': 18.7,
        }
    autostart = True
    
    def update(self):
        sequence = self.server.parameters.get('sequencer.sequence')
        previous_sequence = self.server.parameters.get('sequencer.previous_sequence')
        
        value = self.value
        intersection = np.intersect1d(sequence.value, self.sequence_positions.keys())
        if sequence.loop:
            intersection = np.intersect1d(previous_sequence.value, self.sequence_positions.keys())
            if intersection:
                value = self.sequence_positions[intersection[-1]]
        elif intersection:
            self.value = self.sequence_positions[intersection[-1]]
                
        if self.value != value:
            self.value = value
            self.move_absolute(self.value)
        

Parameter = Position
