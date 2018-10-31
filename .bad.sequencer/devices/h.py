from sequencer.devices.yesr_analog_board.device import YeSrAnalogBoard
from sequencer.devices.yesr_analog_board.channel import YeSrAnalogChannel

class H(YeSrAnalogBoard):
    autostart = True
    
    conductor_servername = 'conductor'
    okfpga_servername = 'daisy_ok'
    okfpga_interface = '1541000D38'

    is_master = False

    channels = [
        YeSrAnalogChannel(loc=0, name='DACG00', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=1, name='Clock AOM Phase', mode='auto', manual_output=1.0),
        YeSrAnalogChannel(loc=2, name='DACG02', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=3, name='813H2 pzt H', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=4, name='813H2 pzt V', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=5, name='DACG05', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=6, name='DACG06', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=7, name='DACG07', mode='auto', manual_output=0.0),
        ]

Device = H
