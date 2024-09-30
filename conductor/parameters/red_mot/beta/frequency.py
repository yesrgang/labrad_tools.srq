from conductor.parameter import ConductorParameter
from rf2.devices.beta import Device


class Parameter(ConductorParameter, Device):
    autostart = False
    priority = 1

    def update(self):
        if self.value is not None:
            self.frequency = self.value
