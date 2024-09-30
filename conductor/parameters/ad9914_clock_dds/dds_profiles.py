from conductor.parameter import ConductorParameter
import json
import calc_fnc_box_freq as fnc

class DDS_Profiles(ConductorParameter):
    """ 
    DDS profile consisting of an array of 3 values:
    [frequency (Hz), phase (rad), amplitude (in [0,1])]
    """
    priority = 16 # set these values before the single parameters (-> higher priority)
    autostart = False
    #value_type = 'list'
    value_type = 'data'
    value={'0': [1., 0., 1.]} # dummy dds setting
    
    def initialize(self,config):
	self.connect_to_labrad()

    def update(self):
        if self.value is not None:
            mjm_comb_demod = json.loads(self.cxn.conductor.get_parameter_values(json.dumps({'si21.mjm_comb_demod_frequency':{}})))['si21.mjm_comb_demod_frequency']
            if mjm_comb_demod is None:
                return

            dds_vals=[]
            for key in self.value.keys():
                out_freq = fnc.calc_sr2_fnc_box_ref_freq(mjm_comb_demod, self.value[key][0])
                #print('CLK DDS profile {:d}: '.format(int(key)), self.value[key])
                dds_vals.append([float(key), out_freq, self.value[key][1], self.value[key][2]])

            #print(dds_vals)
            self.cxn.yesr14_ad9914.clear_programmable_modulus_mode()
            self.cxn.yesr14_ad9914.save_new_profiles(dds_vals)
            #self.cxn.yesr14_ad9914.program_profiles(dds_vals)

            #request = {
            #        'yesr14_ad9914.set_profile': vals,
            #        }
            #self.server._set_parameter_values(request)
            #self.cxn.yesr14_ad9914.set_profile(vals)


Parameter = DDS_Profiles
