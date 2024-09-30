from conductor.parameter import ConductorParameter
import vxi11

class Parameter(ConductorParameter):
    priority = 1
    autostart = False
    def initialize(self, config):
        self.inst = vxi11.Instrument('128.138.107.33')
        self.inst.timeout = 1
    
    def update(self):
        try:
            response = self.inst.ask('SOUR1:FREQ?')
            self.inst.local()
            self.value = 8 * float(response)
        except Exception as e:
            print('mjm_comb_demod_frequency error ! Check the following error message!')
            print(e)

#    def update(self):
##        self.inst.lock()
#        response = self.inst.ask('SOUR1:FREQ?')
#        self.inst.local()
##        self.inst.unlock()
#        self.value = 8 * float(response)
