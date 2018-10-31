from rf.devices.ag335xxx.device import AG335xxx

def cancel_delayed_calls(device):
    for call in device.delayed_calls:
        if call.active():
            call.cancel()
    device.delayed_calls = []

class ClockDedrift(AG335xxx):
    vxi11_address = "192.168.1.18"
    source = 1
    
    amplitude_units = 'V'
    amplitude_range = (0, 0.5)
    
    frequency_range = (20e3, 30e6)

    counter_name = 'clock_dedrift'
    ramp_duration = 8000
    delayed_calls = []
    
    def initialize(self):
        AG335xxx.initialize(self)
        self.vxi11.write('SOUR1:FUNC SIN')
        self.vxi11.write('SOUR1:VOLT 500e-3')
        self.vxi11.write('SOUR1:VOLT:OFFS 0')
        self.vxi11.write('OUTP1 1')

        self.connect_to_labrad()
        self.frequency_counter = self.cxn['frequency_counter']

    def get_ramprate(self):
        start_command = 'SOUR{}:FREQ:STAR?'.format(self.source)
        stop_command = 'SOUR{}:FREQ:STOP?'.format(self.source)
        time_command = 'SOUR{}:SWEEp:TIME?'.format(self.source)
        f_start = self.vxi11.ask(start_command)
        f_stop = self.vxi11.ask(stop_command)
        t_ramp = self.vxi11.ask(time_command)
        ramprate = (float(f_stop) - float(f_start)) / float(t_ramp)
        return ramprate
    
    def set_ramprate(self, ramprate):
        cancel_delayed_calls(self)
        request = {self.counter_name: None}
        response_json = self.frequency_counter.frequency(json.dumps(request))
        response = json.loads(response_json)
        frequency = response[self.counter_name]
        f_start = frequency
        f_stop = f_start + ramprate * self.ramp_duration
        commands = [
            'SOUR{}:FREQ {}'.format(self.source, f_start),
            'SOUR{}:FREQ:STAR {}'.format(self.source, f_start),
            'SOUR{}:FREQ:STOP {}'.format(self.source, f_stop),
            'SOUR{}:SWEEp:TIME {}'.format(self.source, self.ramp_duration),
            'SOUR{}:FREQ:MODE SWE'.format(self.source),
            'TRIG{}:SOUR IMM'.format(self.source),
        ]
        for command in commands:
            self.vxi11.write(command)
        call = callLater(self.ramp_duration * 0.9, self.set_ramprate, ramprate)
        self.delayed_calls.append(call)

Device = ClockDedrift
