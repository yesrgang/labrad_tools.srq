from conductor.parameter import ConductorParameter
from rf2.devices.sg380 import SG380

class Parameter(ConductorParameter, SG380):
    autostart = False
    priority = 12

    _vxi11_address = '192.168.1.60'

    def update(self):
        if self.value is not None:
            self.frequency = self.value
#            f0 = self.frequency
#            f_final = self.value
#            d_nu = (f_final - f0)/10.
#            for i in range(10):
#                i = i + 1
#                self.frequency = f0 + i*d_nu
