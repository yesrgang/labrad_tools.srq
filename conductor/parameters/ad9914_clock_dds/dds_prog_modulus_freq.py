from conductor.parameter import ConductorParameter
import json
import calc_fnc_box_freq as fnc

class DDS_Prog_Modulus_Freq(ConductorParameter):
    """ 
    Set Programmable Modulus frequency of DDS with uHz resolution
    (prevents use of frequency of profiles!)
    """

    priority = 14 # execute after specifying all profile values
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
            print('AD9914 Programmable Modulus frequency:', out_freq)
            self.cxn.yesr14_ad9914.save_programmable_modulus_frequency(out_freq)

 
Parameter = DDS_Prog_Modulus_Freq
