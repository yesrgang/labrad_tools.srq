from conductor.parameter import ConductorParameter

class DDS_Phase_1(ConductorParameter):
    """ 
    Update phase of DDS profile 1 (phase in rad)
    """

    priority = 15
    autostart = False
    #value_type = 'list'
    #value_type = 'data'
    
    def initialize(self,config):
	self.connect_to_labrad()

    def update(self):
        if self.value is not None:

            print('AD9914 phase 1:', self.value)
            self.cxn.yesr14_ad9914.save_new_phase(1, self.value)

Parameter = DDS_Phase_1
