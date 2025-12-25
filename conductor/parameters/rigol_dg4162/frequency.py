import json
import numpy as np
import time
import os

from conductor.parameter import ConductorParameter


class Frequency(ConductorParameter):
    autostart = True
    priority = 1
    #call_in_thread = True

    # record_types = [
    #         'rabi-clock',
    #         'rabi-clock-x',
    #         'ramsey-dark',
    #         'rabi-clock-cleanup',
    #         'rabi-clock-cleanup-CLKOLPD',
    #         'rabi-clock-x-CLKINTOLL',
    #         'rabi-clock-x-CLKOLPD',
    #         'rabi-rb-start',
    #         ]
    
    def initialize(self, config):
        self.connect_to_labrad()

    def update(self):
        #freq = self.server.parameters.get('sequencer.f_LO-1354')
        #amp = self.server.parameters.get('sequencer.amp_LO-1354')
        # if there is a conductor parameter (LO frequency), execute the one below. 
        #self.value = self.server.parameters.get("sequencer.freq_LO-1354")
        try:
            if self.value is not None:
                #amp_LO = json.loads(self.cxn.conductor.get_parameter_values(json.dumps({'sequencer.amp_LO-1354':{}})))['sequencer.amp_LO-1354']
                amp_LO = self.server.parameters.get("rigol_dg4162.amplitude")
                if amp_LO is None:
                    amp_LO.value = 10
                print("Rigol DG4162 output: {} MHz, {} dBm.".format(self.value/1e6, amp_LO.value))
                #print(type(amp_LO.value))
                self.cxn.yesr14_rigol.set_wf_sine_full(1, self.value, amp_LO.value, 5)
                #self.cxn.yesr13_rigol.connect_dev()
                #self.cxn.yesr13_rigol.initialize_dev()
                #self.cxn.yesr13_rigol.disconnect_dev()
            #else:
               # print("######self.value is None!!######")
        except Exception as e:
            print(e)

Parameter = Frequency
