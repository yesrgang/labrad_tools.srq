from conductor.parameter import ConductorParameter
import json
import calc_fnc_box_freq as fnc

#import sys
#sys.path.append('../../../fpga_dds') # for fpga_dds_sequences.py
#import fpga_dds_sequences as ds

class Sequences(ConductorParameter):
    """ 
    Program FPGA-DDS sequence(s)
    """

    priority = 12 # lowest number -> execute last;  i.e.: program last (after saving all required DDS parameters)

    autostart = False
    value_type = 'single'
    #value_type = 'list' # array
    #value_type = 'data' # dict
    
    def initialize(self,config):
	self.connect_to_labrad()

    def update(self):
        if self.value is not None:
            # calculate ref frequency for fnc box
            mjm_comb_demod = json.loads(self.cxn.conductor.get_parameter_values(json.dumps({'si21.mjm_comb_demod_frequency':{}})))['si21.mjm_comb_demod_frequency']
            if mjm_comb_demod is None:
                return

            freq_offs,freq_mult = fnc.calc_sr2_fnc_box_offs(mjm_comb_demod)

            # program FPGA-DDS
            #self.cxn.yesr13_synthesizer.reset(reset_outputs=True) # abort any running sequence
            self.cxn.yesr13_synthesizer.write_timestamps(self.value, freq_offs, freq_mult, compile=True, verbose=False)
            self.cxn.yesr13_synthesizer.trigger() # just for testing...

 
Parameter = Sequences
