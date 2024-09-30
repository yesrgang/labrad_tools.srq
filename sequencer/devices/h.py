from sequencer.devices.yesr_analog_board.device import YeSrAnalogBoard
from sequencer.devices.yesr_analog_board.channel import YeSrAnalogChannel
#from sequencer.devices.yesr_analog_board2.device import YeSrAnalogBoard
#from sequencer.devices.yesr_analog_board2.channel import YeSrAnalogChannel

class H(YeSrAnalogBoard):
    autostart = True
    
    conductor_servername = 'conductor'
    ok_servername = 'yesr20_ok'
    ok_interface = '1541000D38'

    is_master = False

    channels = [
        YeSrAnalogChannel(loc=0, name='3D1 Intensity', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=1, name='3D2 Intensity', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=2, name='3D3 Intensity', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=3, name='461 detuning', mode='autp', manual_output=-2.0, alt_keys=['461 Detuning@F05', '813 H Mixer@F05', 'DACF05@F05']),
        YeSrAnalogChannel(loc=4, name='Clock Intensity', mode='manual', manual_output=6.0, alt_keys=['Clock Intensity@F04', 'DACF04@F04']),
        YeSrAnalogChannel(loc=5, name='813 H1 Intensity', mode='auto', manual_output=-3.5, alt_keys=['813 H1 Intensity', 'DACF01@F01']),
        YeSrAnalogChannel(loc=6, name='DACH06', mode='manual', manual_output=-1.0),
        YeSrAnalogChannel(loc=7, name='813 V Intensity', mode='auto', manual_output=-5.0, alt_keys=['813 V Intensity@F03', 'DACF03@F03']),
        ]

Device = H
