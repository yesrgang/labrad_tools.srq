import json
import os
import time

import labrad
from twisted.internet.reactor import callInThread
from twisted.internet.reactor import callFromThread

from conductor.parameter import ConductorParameter
from ok_server.proxy import OKProxy

class Sequence(ConductorParameter):
    autostart = True
    priority = 10
    value_type = 'list'
    value = ['all_off'] * 1

    loop = True
    call_in_thread = False

    ok_master_servername = 'yesr20_ok'
    ok_master_interfacename = '1616000EHA'

    sequencer_servername = 'sequencer'
#    sequencer_devices = ['abcd', 'e', 'f', 'g', 'h', 'v']
    sequencer_devices = ['abcd', 'e', 'g', 'h', 'v']
#    sequencer_devices = ['abcd', 'g', 'h', 'v']

    sequencer_master_device = 'abcd'
    
    def initialize(self, config):
        super(Sequence, self).initialize(config)
#        try:
#            password = os.getenv('SR1LABRADPASSWORD')
#            self.sr1_cxn = labrad.connect(host='yeelmo.colorado.edu', password=password)
#            sr1_timestamp = self.sr1_cxn.time.time()
#        except Exception, e:
#            print e
#            print 'sr1 time server not found'
#            self.sr1_cxn = None

        self.connect_to_labrad()
        self.ok_server = getattr(self.cxn, self.ok_master_servername)
        self.sequencer_server = getattr(self.cxn, self.sequencer_servername)

        ok = OKProxy(self.ok_server)
        fp = ok.okCFrontPanel()
        fp.OpenBySerial(self.ok_master_interfacename)
        self.fp = fp

        request = {device_name: {} for device_name in self.sequencer_devices}
#        self.sequencer_server.reload_devices(json.dumps(request))
        self.sequencer_server.initialize_devices(json.dumps(request))
        self.previous_sequencer_parameter_values = self._get_sequencer_parameter_values()
        callInThread(self.update)
    
    def update(self):
        """ value is list of strings """
        # first check if we are running
        request = {self.sequencer_master_device: None}
        response = json.loads(self.sequencer_server.running(json.dumps(request)))
        running = response.get(self.sequencer_master_device)
        if not running:
            request = {device_name: self.value for device_name in self.sequencer_devices}
            self.sequencer_server.sequence(json.dumps(request))
            request = {device_name: True for device_name in self.sequencer_devices}
            self.sequencer_server.running(json.dumps(request))
            if not self.loop:
                request = {device_name: False for device_name in self.sequencer_devices}
                self.sequencer_server.running(json.dumps(request))

        if self.loop:
            print(1)
            # then check what sequence is running
            request = {device_name: None for device_name in self.sequencer_devices}
            what_is_running = json.loads(self.sequencer_server.sequence(json.dumps(request)))
            what_i_think_is_running = {
                device_name: self.value 
                    for device_name in self.sequencer_devices
                } 
            current_sequencer_parameter_values = self._get_sequencer_parameter_values()
            #if (what_i_think_is_running != what_is_running) or (
            #        self.previous_sequencer_parameter_values != current_sequencer_parameter_values):
            if (what_i_think_is_running != what_is_running):
                request = what_i_think_is_running
                self.sequencer_server.sequence(json.dumps(request))
                self.server.experiment['repeat_shot'] = True
            else:
                print(1)
                nv = self.next_value
                print(2)
                request = {device_name: nv for device_name in self.sequencer_devices}
                print(3)
                self.sequencer_server.sequence(json.dumps(request))
                #self.sequencer_server.set_sequence_fast(json.dumps(request))
                print(4)

        if (not self.loop) and running:
            raise Exception('something is wrong with sequencer.sequence')
         
        callInThread(self._advance_on_trigger)
        #self._advance_on_trigger()

    def _get_sequencer_parameter_values(self):
        active_parameters = self.server._get_active_parameters()
        active_sequencer_parameters = [pn for pn in active_parameters if pn.find('sequencer.') == 0]
        request = {pn: None for pn in active_sequencer_parameters}
        sequencer_parameter_values = self.server._get_parameter_values(request)
        return sequencer_parameter_values

    def _wait_for_trigger(self):
        # clear trigger
        self.fp.UpdateTriggerOuts()
        is_triggered = self.fp.IsTriggered(0x60)
    
        while True:
            self.fp.UpdateTriggerOuts()
            is_triggered = self.fp.IsTriggered(0x60)
            if is_triggered:
                return
            time.sleep(0.01)

    def _advance_on_trigger(self):
        print('seq waiting')
        self._wait_for_trigger()
        print('seq done waiting')
#        self.fp._wait_trigger(0x60)
        self._mark_timestamp()
        #self.server._advance()
        conductor_server = getattr(self.cxn, 'conductor')
        conductor_server.advance(True)

    def _mark_timestamp(self):
        request = {'timestamp': time.time()}
#        if self.sr1_cxn is not None:
#            sr1_timestamp = self.sr1_cxn.time.time()
#            request.update({'sr1_timestamp': sr1_timestamp})
        conductor_server = self.cxn.conductor
        conductor_server.set_parameter_values(json.dumps(request))

Parameter = Sequence
