import numpy as np

from conductor.parameter import ConductorParameter
from elliptec.devices import h1_retro_block


class Parameter(ConductorParameter, h1_retro_block.Device):
    priority = 1
    autostart = False
    
    def update(self):
        if self.value is not None:
            self.blocked = self.value
