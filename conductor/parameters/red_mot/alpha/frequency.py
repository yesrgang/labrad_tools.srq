from conductor.parameter import ConductorParameter
from rf2.devices.alpha import Device

class Parameter(ConductorParameter, Device):
    autostart = False
    priority = 1

    def update(self):
        self.value = self.frequency
