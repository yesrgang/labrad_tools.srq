from conductor.parameter import ConductorParameter

class DDS_Amplitude_2(ConductorParameter):
    """ 
    Update amplitude of DDS profile 2 (in [0,1])
    """

    priority = 14
    autostart = False
    #value_type = 'list'
    #value_type = 'data'
    
    def initialize(self,config):
	self.connect_to_labrad()

    def update(self):
        if self.value is not None:

            print('AD9914 amplitude 2:', self.value)
            self.cxn.yesr14_ad9914.save_new_amplitude(2, self.value)

Parameter = DDS_Amplitude_2
