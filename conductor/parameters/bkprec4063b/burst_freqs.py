from conductor.parameter import ConductorParameter
import json
import bkprec_4063b as bkp
import socket



class Burst_Params(ConductorParameter):
    """ 
    Set output of BKPrecision 4063B function generator to sine burst
    """

    priority = 15
    autostart = False
    #value_type = 'list'
    #value_type = 'data'
    
    def initialize(self, config):
	self.connect_to_labrad()

        self.oldval = None

        # initialize connection to function generator
        bkprec4063b_host = '192.168.1.236'
        bkprec4063b_port = 5024 # SCPI telnet
        self._bkprec_conn_details = (bkprec4063b_host, bkprec4063b_port)

    def update(self):
        if self.value is not None:
            if (self.oldval is None) or (self.value != self.oldval):
                #self.oldval = self.value
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect(self._bkprec_conn_details)
                    # it's important to set the timeout because if the device does not return data properly
                    # the recv() function will block indefinitely
                    s.settimeout(1) # (in s)

                    dev = bkp.BKPrec4063B(s)
                    dev.send_cmd(b'C2:OUTP OFF')

                    # sine wave
                    dev.send_cmd(b'C2:BSWV WVTP,SINE')
                    #dev.send_cmd(b'C2:BSWV FRQ,10000Hz')
                    dev.send_cmd(b'C2:BSWV FRQ,{:.6f}Hz'.format(self.value))
                    dev.send_cmd(b'C2:BSWV AMP,1Vpp')
                    dev.send_cmd(b'C2:BSWV OFST,0V')
                    dev.send_cmd(b'C2:BSWV PHSE,0')

                    # gated burst
                    dev.send_cmd(b'C2:BTWV STATE,ON')
                    dev.send_cmd(b'C2:BTWV GATE_NCYC,GATE')
                    dev.send_cmd(b'C2:BTWV TRSR,EXT')
                    dev.send_cmd(b'C2:BTWV PLRT,POS')
                    dev.send_cmd(b'C2:BTWV STPS,0')

                    dev.send_cmd(b'C2:OUTP ON,HZ')
                except Exception as e:
                    print(e)
                    s.close()

 
Parameter = Burst_Params
