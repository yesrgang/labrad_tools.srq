from conductor.parameter import ConductorParameter
import json
import sys
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

            # program FPGA-DDS
            try:
                # calculate ref frequency for fnc box
                mjm_comb_demod = json.loads(self.cxn.conductor.get_parameter_values(json.dumps({'si21.mjm_comb_demod_frequency':{}})))['si21.mjm_comb_demod_frequency']
                if mjm_comb_demod is None:
                    print('MJM-comb demod value not ready - FPGA-DDS not programmed!')

                # retrieve verbosity setting for FPGA-DDS programming
                try: # in case fpga_dds.verbose does not exist
                    if json.loads(self.cxn.conductor.get_parameter_values('{"fpga_dds.verbose":{}}'))['fpga_dds.verbose'] == 1:
                        verbose = True
                    else:
                        verbose = False
                except:
                    verbose = False

                self.cxn.yesr13_fpgadds.reset(True) # abort any running sequence (+ clear timestamp memory)
                if not mjm_comb_demod is None:
                    freq_offs,freq_mult = fnc.calc_sr2_fnc_box_offs(mjm_comb_demod)

                    self.cxn.yesr13_fpgadds.write_timestamps(self.value, freq_offs, freq_mult, True, verbose)
                    #self.cxn.yesr13_fpgadds.trigger() # just for testing...


            except Exception as e:
                sys.stdout.write('FPGA-DDS ERROR:\n  ')
                sys.stdout.flush()
                print(e)

 
Parameter = Sequences
