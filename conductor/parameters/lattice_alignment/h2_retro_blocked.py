from conductor.parameter import ConductorParameter
from _serial import SerialProxy


class Parameter(ConductorParameter):
    priority = 1
    autostart = False

#    def initialize(self, config):
#        print('init h2')
#        serial = SerialProxy(('192.168.1.91', 42922))
#        self._ser = serial.Serial('COM4', timeout=0.2)
#        print('done init h2')
#
#    def terminate(self):
#        self._ser.close()
#    
#    def update(self):
#        if self.value:
#            self._ser.write(b'0fw\r\n')
#        else:
#            self._ser.write(b'0bw\r\n')
