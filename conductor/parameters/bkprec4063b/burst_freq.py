from conductor.parameter import ConductorParameter
import json
import bkprec_4063b as bkp
import socket



class Burst_Freq(ConductorParameter):
    """ 
    Set output of BKPrecision 4063B function generator to sine burst
    """

    priority = 15
    autostart = False
    #value_type = 'list'
    #value_type = 'data'
    
    def initialize(self, config):
	self.connect_to_labrad()

        # initialize connection to function generator
        bkprec4063b_host = '192.168.1.236'
        bkprec4063b_port = 5024 # SCPI telnet

    def terminate(self):
        print('BKPrec-Burst_Freq: Urgh, so cold...')

    def update(self):
        #if self.value is not None:
        #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #  s.connect((bkprec4063b_host, bkprec4063b_port))
        #  # it's important to set the timeout because if the device does not return data properly
        #  # the recv() function will block indefinitely
        #  s.settimeout(1) # (in s)

        #  dev = bkp.BKPrec4063B(s)
        #  print(dev.send_cmd(b'*IDN'))
        #  print(dev.send_cmd(b'C2:OUTP OFF'))

        #  # sine wave
        #  print(dev.send_cmd(b'C2:BSWV WVTP,SINE'))
        #  print(dev.send_cmd(b'C2:BSWV FRQ,10000Hz'))
        #  print(dev.send_cmd(b'C2:BSWV AMP,1Vpp'))
        #  print(dev.send_cmd(b'C2:BSWV OFST,0V'))
        #  print(dev.send_cmd(b'C2:BSWV PHSE,0'))

        #  # gated burst
        #  print(dev.send_cmd(b'C2:BTWV STATE,ON'))
        #  print(dev.send_cmd(b'C2:BTWV GATE_NCYC,GATE'))
        #  print(dev.send_cmd(b'C2:BTWV TRSR,EXT'))
        #  print(dev.send_cmd(b'C2:BTWV PLRT,NEG'))
        #  print(dev.send_cmd(b'C2:BTWV STPS,0'))

        #  print(dev.send_cmd(b'C2:OUTP ON,HZ'))
        #    # calculate ref frequency for fnc box
        #    mjm_comb_demod = json.loads(self.cxn.conductor.get_parameter_values(json.dumps({'si21.mjm_comb_demod_frequency':{}})))['si21.mjm_comb_demod_frequency']
        #    if mjm_comb_demod is None:
        #        return

        #    out_freq = fnc.calc_sr2_fnc_box_ref_freq(mjm_comb_demod, self.value)
        #    print('AD9914 frequency 0:', out_freq)
        #    self.cxn.yesr14_ad9914.clear_programmable_modulus_mode()
        #    self.cxn.yesr14_ad9914.save_new_frequency(0, out_freq)

 
Parameter = Burst_Freq
