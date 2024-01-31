from conductor.parameter import ConductorParameter
from rf2.devices.agilent33500 import Agilent33500

class Parameter(ConductorParameter, Agilent33500):
    _vxi11_address = '192.168.1.99'
    _source = 1
    priority = 1

    def update(self):
        if self.value is not None:
            self.frequency = self.value
