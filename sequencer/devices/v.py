from sequencer.devices.yesr_analog_board.device import YeSrAnalogBoard
from sequencer.devices.yesr_analog_board.channel import YeSrAnalogChannel

class V(YeSrAnalogBoard):
    autostart = True
    
    conductor_servername = 'conductor'
    ok_servername = 'yesr9_ok'
    ok_interface = '1840000NUA'
    
    is_master = False

    channels = [
        YeSrAnalogChannel(loc=0, name='V - Alpha Intensity', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=1, name='V - Beta Intensity', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=2, name='V - Spin Pol. Intensity', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=3, name='V - Alpha FM', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=4, name='V - Beta FM', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=5, name='V - ', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=6, name='V - ', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=7, name='V - ', mode='auto', manual_output=0.0),
        ]


Device = E
