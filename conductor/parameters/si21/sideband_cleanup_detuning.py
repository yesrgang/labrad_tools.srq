from conductor.parameter import ConductorParameter

class CleanupDetuning(ConductorParameter):
    """ detuning of the 1716882'th tooth of the frequency comb, when locked to 
    Si21 cavity of the atomic probe
    """
    #priority = 3
    priority = 13
    autostart = True
    
    visible_tooth = 1716882.0
    ir_comb_tooth = 777577.0
    f_sr = 429.228005229873e12
    f_rep = 250.0044673155e6
    f_ceo = 35e6

    def initialize(self,config):
	self.connect_to_labrad()

    def update(self):
        if self.value is not None:
            # Demod frequency of mjm-comb beat note. The MJM laser sits below 
            # the comb tooth it is locked to. Thus, if the frequency of the MJM 
            # laser is increases, this number decreases.
            mjm_comb_demod = self.server._get_parameter_value(
                    'si21.mjm_comb_demod_frequency')
            if mjm_comb_demod is None:
                return
            
            # aom on comb table. 0th order goes to comb. double passed, +1 order 
            # goes back through fiber.
            comb_table_offset_aom = 30.0e6

            # beat frequency for distribution center -> comb table fiber noise 
            # cancellation.
            comb_dist_fnc_beat = -95.524640e6

            # implied frequency of aom between distribution center and comb.
            # light travelling from distribution center to comb table is shifted 
            # down in frequency.
            comb_dist_aom = (comb_dist_fnc_beat - 2.0 * comb_table_offset_aom) / 2.0
            
            # frequency of the injection locked diode in the distribution center,
            # relative to the stable comb tooth.
            dist_diode = -comb_dist_aom - mjm_comb_demod
            
            # between diode and atoms
            srq_dist_fnc = self.value - dist_diode

            # 100 MHz AOM after fiber on SrQ table.
            srq_table_offset_aom = -100e6

            # fix output of FNC box VCO to 77.77 MHz
            srq_dist_aom = -77.77e6

            # second aom on SrQ table to keep FNC VCO within output bandwidth.
            srq_steer = srq_dist_aom + srq_table_offset_aom - srq_dist_fnc

            srq_dist_fnc_demod = -2 * srq_dist_fnc

            request = {
#                'clock_aom.frequency': float(srq_steer),
#                'clock_fiber_aom.demod_frequency': float(srq_dist_fnc),
#                'clock_fiber_aom.demod_cleanup_frequency': float(-2 * srq_dist_fnc),
                'clock_fiber_aom.demod_sideband_cleanup_frequency': float(-2 * srq_dist_fnc),
                }
            self.server._set_parameter_values(request)
        

Parameter = CleanupDetuning
