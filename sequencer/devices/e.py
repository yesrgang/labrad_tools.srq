from sequencer.devices.yesr_analog_board2.device import YeSrAnalogBoard
from sequencer.devices.yesr_analog_board2.channel import YeSrAnalogChannel

class E(YeSrAnalogBoard):
    autostart = True
    
    conductor_servername = 'conductor'
    ok_servername = 'yesr20_ok'
    ok_interface = '14290008VV'
    
    is_master = False

    channels = [
        YeSrAnalogChannel(loc=0, name='DACE00', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=1, name='DACE01', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=2, name='DACE02', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=3, name='DACE03', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=4, name='DACE04', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=5, name='DACE05', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=6, name='DACE06', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=7, name='DACE07', mode='auto', manual_output=0.0),
        ]


Device = E
