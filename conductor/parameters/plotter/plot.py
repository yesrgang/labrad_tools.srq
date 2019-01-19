import json
import traceback

from conductor.parameter import ConductorParameter

class Plot(ConductorParameter):
    autostart = False
    priority = 1
    call_in_thread = True
    value_type = 'dict'
    
    plotter_servername = 'plotter'

    
    def initialize(self,config):
        self.connect_to_labrad()
    
    def update(self):
        experiment_name = self.server.experiment.get('name')

        if self.value and (experiment_name is not None):
            self.value['data_path'] = experiment_name
            self.cxn.plotter.plot(json.dumps(self.value))

Parameter = Plot
