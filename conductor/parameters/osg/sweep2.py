from conductor.parameter import ConductorParameter
from rf2.devices.osg_sweep2 import Device

class Parameter(ConductorParameter, Device):
    priority = 1
    autostart = False

    def initialize(self, config):
        ConductorParameter.initialize(self, config)
        self.start_frequency = 68.9025e6
    
    def update(self):
        if self.value is not None:
            self.stop_frequency = self.value
