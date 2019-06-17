from sequencer.devices.yesr_analog_board.device import YeSrAnalogBoard
from sequencer.devices.yesr_analog_board.channel import YeSrAnalogChannel

class H(YeSrAnalogBoard):
    autostart = True
    
    conductor_servername = 'conductor'
    ok_servername = 'yesr20_ok'
    ok_interface = '1541000D38'

    is_master = False

    channels = [
        YeSrAnalogChannel(loc=0, name='DACH00', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=1, name='DACH01', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=2, name='DACH02', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=3, name='DACH03', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=4, name='DACH04', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=5, name='DACH05', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=6, name='DACH06', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=7, name='DACH07', mode='auto', manual_output=0.0),
        ]

Device = H
