from conductor.parameter import ConductorParameter
import rf2.devices.clock_demod_sideband_cleanup
reload(rf2.devices.clock_demod_sideband_cleanup)
from rf2.devices.clock_demod_sideband_cleanup import Device

class Parameter(ConductorParameter, Device):
    autostart = False
    priority = 12

    def update(self):
        if self.value is not None:
            self.frequency = self.value
