from conductor.parameter import ConductorParameter

class Clock_DDS_Profile0(ConductorParameter):
    """ 
    DDS profile 0 consisting of an array of 3 values:
    [frequency (Hz), phase (rad), amplitude (in [0,1])]
    """
    #priority = 3
    priority = 13
    autostart = True
    
    def initialize(self,config):
	    self.connect_to_labrad()

    def update(self):
        if self.value is not None:

            print('aaaa param:', self.value)
            #request = {
#           #     'clock_aom.frequency': float(srq_steer),
#           #     'clock_fiber_aom.demod_frequency': float(srq_dist_fnc),
            #    'clock_fiber_aom.demod_cleanup_frequency': float(-2 * srq_dist_fnc),
            #    }
            #self.server._set_parameter_values(request)
        

Parameter = Clock_DDS_Profile0
