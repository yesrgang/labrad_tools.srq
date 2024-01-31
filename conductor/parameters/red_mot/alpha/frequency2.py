#import numpy as np
#
#from conductor.parameter import ConductorParameter
#import rf2.devices.clock_demod_sideband_cleanup
#reload(rf2.devices.clock_demod_sideband_cleanup)
#from rf2.devices.clock_demod_sideband_cleanup import Device
#
#
#class Parameter(ConductorParameter, Device):
#    autostart = False
#    priority = 12
#
#    def update(self):
#        if self.value is not None:
##            self.frequency = self.value
#            next_freq = self.value
#            prev_freq = self.frequency
#            freq_diff = next_freq - prev_freq
#            if freq_diff != 0: 
#                freqs = np.linspace(prev_freq, next_freq, np.ceil(abs(freq_diff) / 1e6) + 1)
#                for f in freqs:
#                    self.frequency = f
#                print('done setting blue_imaging_detuning')

from conductor.parameter import ConductorParameter
from rf2.devices.sg380 import SG380

class ConductorParameter(SG380):
    _vxi11_address = '192.168.1.63'
    autostart = False
    priority = 1

    def update(self):
        if self.value is not None:
            self.frequency = self.value
