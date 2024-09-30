from conductor.parameter import ConductorParameter
from rf2.devices.sg380 import SG380

class Parameter(ConductorParameter, SG380):
    autostart = False
    priority = 12

    _vxi11_address = '192.168.1.94'

    def update(self):
        if self.value is not None:
            self.amplitude = self.value
