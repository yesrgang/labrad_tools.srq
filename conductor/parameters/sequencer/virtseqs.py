from conductor.parameter import ConductorParameter
import json
import sys


class Virtseqs(ConductorParameter):
    """ 
    Transfer sequence dictionaries to Sequencer which are not saved in a file but just in
    a variable ("virtual sequences"): sequencer.virtseqs
    """

    priority = 11 # lowest number -> execute last;  i.e.: program last (after saving all required DDS parameters)
                  # trigger before sequencer.sequence

    autostart = False
    #value_type = 'single'
    #value_type = 'list' # array
    value_type = 'data' # dict


    sequencer_servername = 'sequencer'
    
    def initialize(self,config):
	self.connect_to_labrad()
        self.sequencer_server = getattr(self.cxn, self.sequencer_servername)

    def update(self):
        if self.value is not None:
            self.sequencer_server.set_virtual_sequences(json.dumps(self.value))

 
Parameter = Virtseqs
