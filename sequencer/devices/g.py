from sequencer.devices.yesr_analog_board.device import YeSrAnalogBoard
from sequencer.devices.yesr_analog_board.channel import YeSrAnalogChannel
#from sequencer.devices.yesr_analog_board2.device import YeSrAnalogBoard
#from sequencer.devices.yesr_analog_board2.channel import YeSrAnalogChannel

class G(YeSrAnalogBoard):
    autostart = True
    
    conductor_servername = 'conductor'
    ok_servername = 'yesr20_ok'
    ok_interface = '1541000D3G'
    
    is_master = False

    channels = [
        YeSrAnalogChannel(loc=0, name='Z Comp. Coil', mode='auto', manual_output=0.0, alt_keys=['Z Comp. Coil@E04', 'DACE04@E04']),
        YeSrAnalogChannel(loc=1, name='Y Comp. Coil', mode='auto', manual_output=0.0, alt_keys=['Y Comp. Coil@E03', 'DACE03@E03']),
        YeSrAnalogChannel(loc=2, name='X Comp. Coil', mode='auto', manual_output=0.0, alt_keys=['X Comp. Coil@E02', 'DACE02@E02']),
        YeSrAnalogChannel(loc=3, name='VODT Intensity', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=4, name='813 H2 Intensity', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=5, name='MOT Coil', mode='auto', manual_output=0.0, alt_keys=['MOT Coil@E05', 'DACE05@E05']),
        YeSrAnalogChannel(loc=6, name='HODT Intensity', mode='auto', manual_output=0.0),
        YeSrAnalogChannel(loc=7, name='DACG07', mode='auto', manual_output=0.0),
        ]

Device = G
