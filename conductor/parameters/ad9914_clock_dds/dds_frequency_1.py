from conductor.parameter import ConductorParameter
import json
import calc_fnc_box_freq as fnc

class DDS_Frequency_1(ConductorParameter):
    """ 
    Update amplitude of DDS profile 1 (in [0,1])
    """

    priority = 15
    autostart = False
    #value_type = 'list'
    #value_type = 'data'
    
    def initialize(self,config):
	self.connect_to_labrad()
    def update(self):
        if self.value is not None:
            # calculate ref frequency for fnc box
            mjm_comb_demod = json.loads(self.cxn.conductor.get_parameter_values(json.dumps({'si21.mjm_comb_demod_frequency':{}})))['si21.mjm_comb_demod_frequency']
            if mjm_comb_demod is None:
                return

            out_freq = fnc.calc_sr2_fnc_box_ref_freq(mjm_comb_demod, self.value)
            print('AD9914 frequency 1:', out_freq)
            self.cxn.yesr14_ad9914.clear_programmable_modulus_mode()
            self.cxn.yesr14_ad9914.save_new_frequency(1, out_freq)

 
Parameter = DDS_Frequency_1
