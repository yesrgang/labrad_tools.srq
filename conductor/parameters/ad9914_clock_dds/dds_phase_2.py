from conductor.parameter import ConductorParameter

class DDS_Phase_2(ConductorParameter):
    """ 
    Update phase of DDS profile 2 (phase in rad)
    """

    priority = 15
    autostart = False
    #value_type = 'list'
    #value_type = 'data'
    
    def initialize(self,config):
	self.connect_to_labrad()

    def update(self):
        if self.value is not None:

            print('AD9914 phase 2:', self.value)
            self.cxn.yesr14_ad9914.save_new_phase(2, self.value)

Parameter = DDS_Phase_2
