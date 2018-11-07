import json

from conductor.parameter import ConductorParameter


class Power(ConductorParameter):
    autostart = False
    priority = 1
    value = None
    call_in_thread = True

    current_controller_servername = 'current_controller'
    current_controller_devicename = '3d'
    
    def initialize(self, config):
        super(Power, self).initialize(config)
        self.connect_to_labrad()
        self.current_controller_server = getattr(
            self.cxn, self.current_controller_servername)
    
    def update(self):
        request = {self.current_controller_devicename: None}
        response = json.loads(self.current_controller_server.powers(json.dumps(request)))
        self.value = response[self.current_controller_devicename]

Parameter = Power
