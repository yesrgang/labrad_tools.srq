from sequencer.devices.yesr_analog_board.device import YeSrAnalogBoard
from sequencer.devices.yesr_analog_board.channel import YeSrAnalogChannel

class F(YeSrAnalogBoard):
    autostart = True
    
    conductor_servername = 'conductor'
    ok_servername = 'yesr20_ok'
    ok_interface = '1401000AT3'
    
    is_master = False

    channels = [
        YeSrAnalogChannel(loc=0, name='DACF00', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=1, name='DACF01', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=2, name='DACF02', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=3, name='DACF03', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=4, name='DACF04', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=5, name='DACF05', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=6, name='DACF06', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=7, name='DACF07', mode='auto', manual_output=0.0),
        ]


Device = F
