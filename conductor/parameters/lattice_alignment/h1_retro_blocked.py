from conductor.parameter import ConductorParameter
from _serial import SerialProxy


class Parameter(ConductorParameter):
    priority = 1
    autostart = False

#    def initialize(self, config):
#        print('init h1')
#        serial = SerialProxy(('192.168.1.91', 42922))
#        self._ser = serial.Serial('COM3', timeout=0.5)
#        print('done init h1')
#
#    def terminate(self):
#        self._ser.close()
#    
#    def update(self):
#        if self.value == True:
#            self._ser.write(b'0bw\r\n')
#        elif self.value == False:
#            self._ser.write(b'0fw\r\n')
#        self.value = None
#           
