from conductor.parameter import ConductorParameter

class Program_DDS(ConductorParameter):
    """ 
    Apply all new profiles saved at DDS labrad server
    """

    priority = 13 # lowest number -> execute last;  i.e.: program last (after saving all required DDS parameters)
    autostart = False
    #value_type = 'list'
    #value_type = 'data'
    
    def initialize(self,config):
	self.connect_to_labrad()

    def update(self):
        if self.value is not None:

            if self.value == 1:
                print('programming AD9914 DDS ...')
                self.cxn.yesr14_ad9914.program_new_dds_profiles()

Parameter = Program_DDS
