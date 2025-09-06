from conductor.parameter import ConductorParameter
#import vxi11
import urllib2 # for python 2 compatibility


def get_frequency(url="http://128.138.107.123:8080"):
    try:
        return float(urllib2.urlopen(url, timeout=0.1).read().strip())
    except:
        return None


class Parameter(ConductorParameter):
    priority = 1
    autostart = True
    #def initialize(self, config):
    #    self.inst = vxi11.Instrument('128.138.107.33')
    #    self.inst.timeout = 1
    
    def update(self):
        try:
            #response = self.inst.ask('SOUR1:FREQ?')
            #self.inst.local()
            #self.value = 8 * float(response)
            self.value = 8*get_frequency()
            print('MJM demod frequency: {:.6f} MHz'.format(self.value*1e-6))
        except Exception as e:
            print('mjm_comb_demod_frequency error ! Check the following error message!')
            print(e)

#    def update(self):
##        self.inst.lock()
#        response = self.inst.ask('SOUR1:FREQ?')
#        self.inst.local()
##        self.inst.unlock()
#        self.value = 8 * float(response)
