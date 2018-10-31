from sequencer.devices.yesr_analog_board.device import YeSrAnalogBoard
from sequencer.devices.yesr_analog_board.channel import YeSrAnalogChannel

class F(YeSrAnalogBoard):
    autostart = True
    
    conductor_servername = 'conductor'
    ok_servername = 'yesr20_ok'
#    ok_device_id = 'srq analog 2'
    ok_interface = '1401000AT3'
    
    is_master = False

    channels = [
        YeSrAnalogChannel(loc=0, name='Beta FM', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=1, name='813 H1 Intensity', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=2, name='813 H2 Intensity', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=3, name='813 V Intensity', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=4, name='Clock Intensity', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=5, name='813H Mixer', mode='manual', manual_output=-2.0),
        YeSrAnalogChannel(loc=6, name='813V Mixer', mode='manual', manual_output=-2.0),
        YeSrAnalogChannel(loc=7, name='Spin Pol. Intensity', mode='auto', manual_output=0.0),
        ]


Device = F
