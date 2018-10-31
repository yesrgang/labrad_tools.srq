import json
import time

from twisted.internet.reactor import callInThread

from conductor.parameter import ConductorParameter

class Sequence(ConductorParameter):
    autostart = True
    priority = 10
    value_type = 'list'
    value = ['all_off'] * 1

    loop = True

    okfpga_master_servername = 'daisy_ok'
    okfpga_master_interfacename = '14290008VW'

    sequencer_servername = 'sequencer'
    sequencer_devices = ['abcd', 'h']
    sequencer_master_device = 'abcd'
    
    def initialize(self, config):
        super(Sequence, self).initialize(config)
        self.connect_to_labrad()
        self.okfpga_server = getattr(self.cxn, self.okfpga_master_servername)
        self.sequencer_server = getattr(self.cxn, self.sequencer_servername)
        request = {device_name: {} for device_name in self.sequencer_devices}
        self.sequencer_server.reload_devices(json.dumps(request))
        self.update()
    
    def update(self):
        """ value is list of strings """
        # first check if we are running
        request = {self.sequencer_master_device: None}
        response = json.loads(self.sequencer_server.running(json.dumps(request)))
        running = response.get(self.sequencer_master_device)
        if not running:
            request = {device_name: self.value for device_name in self.sequencer_devices}
            print request
            self.sequencer_server.sequence(json.dumps(request))
            request = {device_name: True for device_name in self.sequencer_devices}
            self.sequencer_server.running(json.dumps(request))
            if not self.loop:
                request = {device_name: False for device_name in self.sequencer_devices}
                self.sequencer_server.running(json.dumps(request))

        if self.loop:
            # then check what sequence is running
            request = {device_name: None for device_name in self.sequencer_devices}
            what_is_running = json.loads(self.sequencer_server.sequence(json.dumps(request)))
            what_i_think_is_running = {
                device_name: self.value 
                    for device_name in self.sequencer_devices
                } 
            if what_i_think_is_running != what_is_running:
                request = {device_name: self.value for device_name in self.sequencer_devices}
                self.sequencer_server.sequence(json.dumps(request))
                self.server.experiment['repeat_shot'] = True
            else:
                request = {device_name: self.next_value for device_name in self.sequencer_devices}
                self.sequencer_server.sequence(json.dumps(request))

        if (not self.loop) and running:
            raise Exception('something is wrong with sequencer.sequence')
        
        callInThread(self._advance_on_trigger)

    def _wait_far_trigger(self):
        # clear trigger
        self.okfpga_server.update_trigger_outs(self.okfpga_master_interfacename)
        is_triggered = self.okfpga_server.is_triggered(self.okfpga_master_interfacename, 0x60)
    
        while True:
            self.okfpga_server.update_trigger_outs(self.okfpga_master_interfacename)
            is_triggered = self.okfpga_server.is_triggered(self.okfpga_master_interfacename, 0x60)
            if is_triggered:
                return

    def _advance_on_trigger(self):
        self._wait_far_trigger()
        self.server._advance()

Parameter = Sequence
