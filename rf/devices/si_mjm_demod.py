from rf.devices.ag335xxx.device import AG335xxx

class SiMJMDemod(AG335xxx):
    autostart = False
    vxi11_address = "192.168.1.58"
    source = 1
    
    amplitude_units = 'dBm'
    amplitude_range = (-20, 20)
    
    frequency_range = (1e3, 30e6)

    def initialize(self, config):
        AG335xxx.initialize(self, config)
        self.vxi11.write('SOUR1:VOLT:UNIT dBm')

Device = SiMJMDemod
